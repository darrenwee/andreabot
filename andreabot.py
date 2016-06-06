#!/usr/bin/python

import time
import datetime
import re
import telebot
import logging
from telebot import types

# andreabot modules
#from botlogger import *
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
global announcements
announcements = []

@bot.message_handler(commands = ['start'])
def welcome(message):
    bot.reply_to(message, 'Hi! I\'m AndreaBot. I help Andrea and other FOP comm members disseminate information to important people.')

@bot.message_handler(commands = ['help'])
def helper(message):
    bot.reply_to(message, 'Commands available: /yell, /log, /time')

"""
    /yell <message>
    - sends <message> to all users on the mailing list (controlled by authorized.py)
"""
@bot.message_handler(commands = ['yell'])
def yell(message):
    if message.from_user.id not in getIDs(mailing_list):
        logger.warning('Attempted unauthorized use of /yell by %s' % message.from_user.id)
        bot.reply_to(message, 'Sorry! You aren\'t allowed to use /yell. Tell Darren (@ohdearren) if this is a mistake.')
        return

    logMessage(message)

    # build the timestamp (modify format as necessary)
    # timestamp is pretty and human-readable, 12hr + date
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%I:%M%p, %d %B %Y')

    # strip command word
    #broadcast = '----- MESSAGE BEGIN -----\n' + re.sub('^\/yell\s+', '', message.text)
    broadcast = re.sub('^/yell\s+', '', message.text)

    # append byline
    #broadcast += '\n----- MESSAGE END -----\n' + '\nSent by %s\n@%s' % (whoIs(message.from_user.id), message.from_user.username)
    broadcast += '\n\nSent by %s\n@%s' % (whoIs(message.from_user.id), message.from_user.username)
    broadcast += '\n' + timestamp

    announcements.append(broadcast)
    # send to all recipients
    for recipient in getIDs(mailing_list):
        bot.send_message(recipient, broadcast)

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

logger.info('AndreaBot is listening ...')
bot.polling()
