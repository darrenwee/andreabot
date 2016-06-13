#!/usr/bin/python

import sys
import time
import datetime
import re
import telepot

from telepot.delegate import per_chat_id, create_open

# andreabot modules
from settings_secret import TOKEN
from botlogger import logger
import authorized
import helper

# establish connection to mongodb server
import pymongo
try:
    connection = pymongo.MongoClient('monty', 27017)
    logger.info('Successfully connected to MongoDB daemon')
except pymongo.errors.ConnectionFailure as e:
    logger.error('Failed to connect to MongoDB: %s' % e)
    logger.error('AndreaBot exiting!')
    sys.exit(1)

db = connection['andreabot']
announcements = db['announcements']

def getTime():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S, %d %B %Y ')
    
def getLog(to_return):
    messages = announcements.find().sort( [ ('_id', -1) ] ).limit(to_return)
    delimiter = '======================\n'

    reply = delimiter

    if messages.count() == 0:
        reply += 'No records found.\n' + delimiter
    else:
        for message in messages:
            reply = delimiter + message['message'] + message['timestamp'] + '\n' + reply
        reply += '%d most recent announcements ^' % to_return
        
    return reply

def yell(bot, message, requester_id):
    # deny unauthorized yeller
    if requester_id not in authorized.getMailingList():
        logger.warn('Attempted unauthorized use of /yell by %s' % requester_id)
        bot.sendMessage(requester_id, 'Sorry! You can\'t use this function. Contact Darren @ohdearren if this is a mistake.')
        return

    # deny empty yell
    if re.match('^\s*/yell\s*$', message) != None:
        logger.warn('%s: /yell denied; no message' % authorized.whoIs(requester_id))
        bot.sendMessage(requester_id, 'I need a message to yell! Yell not carried out.')
        return

    # strip the command word
    broadcast = re.sub('^/yell\s+', '', message)

    # append byline
    broadcast += '\n\nSent by %s via yell\n' % (authorized.whoIs(requester_id))

    # add the announcement to the database
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M%p, %d %B %Y')
    announcement_log = {
        'message': broadcast,
        'to': 'all',
        'by': authorized.whoIs(requester_id),
        'timestamp': timestamp,
    }
    announcements.insert_one(announcement_log)
    logger.info('Added yell by %s to database.' % authorized.whoIs(requester_id))

    # talk to the requester
    bot.sendMessage(requester_id, 'Message is propagating now all listeners.')
    for recipient in authorized.getMailingList():
        bot.sendMessage(recipient, broadcast)
        logger.info('%s: Yell propagated to %s (\'%s ...\')' % (authorized.whoIs(requester_id), authorized.whoIs(recipient), broadcast[:60]))

    return

def whisper(bot, message, needAcknowledgement, requester_id):
    # deny empty whisper
    if re.match('^\s*/whisper\s*$', message) != None:
        logger.warn('%s: /whisper denied; no message or groups!' % authorized.whoIs(requester_id))
        bot.sendMessage(requester_id, 'I need a message and group list to whisper! Whisper not carried out.')
        return

    matches = re.match('\s*/whisper\s+([a-zA-Z+]+)\s+(.+)', message)
    groups = matches.group(1) 
    broadcast = matches.group(2)

    group_list = groupArg2List(groups)

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M%p, %d %B %Y')

    if authorized.groupIsValid(group_list):
        broadcast = re.sub('\s*/whisper\s*', '', message)
        broadcast += '\n\nSent by %s via whisper to:\n' % (authorized.whoIs(requester_id))
        broadcast += ', '.join(group_list) + '\n'

        bot.sendMessage(requester_id, 'Message is propagating now to: %s' % ', '.join(group_list))
        # log in database
        announcement_log = {
            'message': broadcast,
            'to': '+'.join(group_list),
            'by': authorized.whoIs(requester_id),
            'timestamp': timestamp,
        }
        announcements.insert_one(announcement_log)
        logger.info('Added whisper by %s to database.' % authorized.whoIs(requester_id))

        # propagate message
        for recipient in authorized.getGroups(group_list):
            bot.sendMessage(recipient, broadcast)
    else:
        # bad group parameters
        bot.sendMessage(requester_id, 'One of your groups is not valid. Check /who for the group names.')
        logger.warn('%s: /whisper denied; invalid group' % authorized.whoIs(requester_id))
    return

def groupArg2List(groupList):
    if '+' not in groupList:
        return [groupList]
    else:
        return re.split(r'\s*+\s*', groupList)

#class AndreaBot(telepot.helper.ChatHandler):
class AndreaBot(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(AndreaBot, self).__init__(*args, **kwargs)
        self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None

#    def __init__(self, seed_tuple, timeout):
#        super(AndreaBot, self).__init__(seed_tuple, timeout)
#        self._count = 0

    def on_chat_message(self, message):
        content_type, chat_type, chat_id = telepot.glance(message)

        command = message['text']
        logger.info('Received \'%s\' from %s' % (command, authorized.whoIs(chat_id)))

        # for '/start'
        if command == '/start':
            self.sendMessage(chat_id, 'Hi! I\'m AndreaBot. I help Andrea and other FOP comm members disseminate information.')
        # /help [<command>]
        elif command == '/help':
            self.sendMessage(chat_id, helper.getNaiveHelp())
        elif command.startswith('/help'):
            keyword = re.match('\s*/help\s+([a-z]+)\s*', command).group(1)
            self.sendMessage(chat_id, helper.getHelp(keyword))
        # /who
        elif command == '/who':
            self.sendMessage(chat_id, authorized.enumerateListeners())
        # /yell
        elif command.startswith('/yell'):
            yell(self, command, chat_id)
        # /whisper
        elif command.startswith('/whisper'):
            whisper(self, command, False, chat_id)
        # /log
        elif command == '/log':
            self.sendMessage(chat_id, getLog(5))
        # /vlog <size>
        elif command.startswith('/vlog'):
            return_size = re.match('\s*/vlog\s+(\d+)', command).group(1)
            self.sendMessage(chat_id, getLog(int(return_size)))
        # /time
        elif command == '/time':
            self.sendMessage(chat_id, getTime())
        # when nothing works
        else:
            self.sendMessage(chat_id, 'Invalid command. Try /help')

        return

logger.info('AndreaBot is listening ...')

bot = AndreaBot(TOKEN)
bot.message_loop()

#bot = telepot.DelegatorBot(TOKEN, [
#    (per_chat_id(), create_open(AndreaBot, timeout=120)),
#])

while 1:
    time.sleep(10)
