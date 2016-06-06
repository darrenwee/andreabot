#!/usr/bin/python

import time
import datetime
import re
import telebot
import logging
from telebot import types

# andreabot modules
#from botlogger import *
from helper import *
from authorized import *
from settings_secret import TOKEN

# spawn AndreaBot
bot = telebot.TeleBot(TOKEN)
#bot = telebot.AsyncTeleBot(TOKEN)

# for console/file logging
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
logging.captureWarnings(True)

# store messages
# TODO convert to persistent storage to enable bot reboot
global announcements
announcements = []
global message_id
message_id = 1

# fingerprinter
global announcementRead
announcementRead = {
}

@bot.message_handler(commands = ['start'])
def welcome(message):
    logMessage(message)
    bot.reply_to(message, 'Hi! I\'m AndreaBot. I help Andrea and other FOP comm members disseminate information to important people.')

@bot.message_handler(commands = ['help'])
def helper(message):
    logMessage(message)

    # naive helper
    if message.text == '/help':
        bot.reply_to(message, getNaiveHelp())
        return

    # command helper
    command = re.match('/help\s+([a-z]+)', message.text).group(1)
    bot.reply_to(message, getHelp(command))

"""
    /name <name>
    - this doesn't actually do anything except record chat IDs to a file
    - for hardcoding of telegram chat ID into authorized module
"""
@bot.message_handler(commands = ['name'])
def getName(message):
    logMessage(message)
    matches = re.match('/name (.+)', message.text)
    logger.info('%s is ID %s' % (matches.group(1), message.from_user.id))

    # don't bother logging if they're already in the address book
    if message.from_user.id in rev_book:
        bot.reply_to(message, 'I already know you! You\'re %s.' % (rev_book.get(message.from_user.id)))
        return
    
    # write out to a text file so I can get it easily
    with open("chat_ids.txt", 'a') as id_file:
        id_file.write('\'%s\': %s,\n' % (matches.group(1), message.from_user.id))

    # acknowledge user
    bot.reply_to(message, 'Thanks %s! Your chat ID is %s.' % (matches.group(1), message.from_user.id))

"""
    /yell <message>
    - sends <message> to all users on the mailing list (controlled by authorized.py)
"""
@bot.message_handler(commands = ['yell'])
def yell(message):
    logMessage(message)

    # deny people who aren't in the mailing list from yelling
    if message.from_user.id not in mailing_list:
        logger.warning('Attempted unauthorized use of /yell by %s' % message.from_user.id)
        bot.reply_to(message, 'Sorry! You aren\'t allowed to use /yell. Tell Darren (@ohdearren) if this is a mistake.')
        return

    # build the timestamp (modify format as necessary)
    # timestamp is pretty and human-readable, 12hr + date
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M%p, %d %B %Y')

    # append message ID
    broadcast = 'Message ID: %d\n\n' % message_id

    # strip command word and append message
    broadcast += re.sub('^/yell\s+', '', message.text)

    # append byline and pretty timestamp
    broadcast += '\n\nSent by %s\n@%s' % (whoIs(message.from_user.id), message.from_user.username)
    broadcast += '\n' + timestamp

    announcements.append(broadcast)
    announcementRead[message_id] = {}

    failed = ''
    # send to all recipients
    for recipient in mailing_list:
        try:
            # successful send to recipient
            logger.info('Yelling at \'%s\': \'%s\'' % (whoIs(recipient), re.sub('^/yell\s+', '', message.text)))
            bot.send_message(recipient, broadcast)
            announcementRead[message_id][whoIs(recipient)] = False
        except Exception:
            # failed to send to recipient
            logger.warn('Failed to yell at \'%s\'' % whoIs(recipient))
            failed += whoIs(recipient) + '\n'

    message_id += 1

    # feedback to sender about failed recipients, if any
    if failed != '':
        bot.reply_to(message, '\nWARNING: yell did not reach the following people\n\n%s' % failed)

"""
    /log
    - returns the most recent 5 announcements in chronological order (most recent last)
"""
@bot.message_handler(commands = ['log'])
def getLog(message):
    logMessage(message)
    
    # get last 0-5 elements of the announcement list
    targets = announcements[-5:]

    # craft the return message
    delimiter = '\n=======================\n'
    reply = delimiter

    for announcement in targets:
        reply += announcement + delimiter

    if reply == delimiter:
        # no records could be found so message begins is purely the delimiter string
        bot.reply_to(message, 'No messages found.')
    else:
        # some records found
        bot.reply_to(message, reply)

"""
    /time
    - returns the bot's time (so that everyone has an agreeable clock)
    - 24hr format w/ date
"""    
@bot.message_handler(commands = ['time'])
def getTime(message):
    logMessage(message)

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S, %d %B %Y ')
    logger.info('Gave timestamp \'%s\' to %s' % (timestamp, whoIs(message.from_user.id)))
    bot.reply_to(message, timestamp)

def logMessage(message):
    logger.info('%s: %s' % (whoIs(message.from_user.id), message.text))

"""
    /read <id>
    - acknowledge received and read message with ID <id>
"""
@bot.message_handler(commands = ['read'])
def read(message):
    target_id = re.match('/read (\d+)', message.text).group(1)

    # catch non-numeric ID
    if target_id == None:
        bot.reply_to(message, 'The message ID should be made of numbers only.')
        return

    # catch bad message ID
    if target_id not in announcementRead:
        bot.reply_to(message, 'Couldn\'t find a message with this ID.')
        return
    
    announcementRead[target_id][whoIs(message.from_user.id)] = True
    bot.reply_to(message, 'Thanks! You have acknowledged message ID %d' % target_id)
    return

"""
    /status <id>
    - returns acknowledgement status of message with ID <id>
"""
@bot.message_handler(commands = ['status'])
def status(message):
    target_id = re.match('/status (\d+)', message.text).group(1)

    # catch non-numeric ID
    if target_id == None:
        bot.reply_to(message, 'The message ID should be made of numbers only.')
        return

    # catch bad message ID
    if target_id not in announcementRead:
        bot.reply_to(message, 'Couldn\'t find a message with this ID.')
        return
   
    seen = 'Acknowledged by:\n'
    notseen = 'Not seen by:\n'
    for recipient in announcementRead[target_id]:
        if announcementRead[target_id][recipient] == False:
            notseen += recipient + '\n'
        else:
            seen += recipient + '\n'

    bot.reply_to(message, seen + '\n' + notseen)
"""
    /vlog
    - prints every announcement sent
"""

logger.info('AndreaBot is listening ...')
bot.polling()
