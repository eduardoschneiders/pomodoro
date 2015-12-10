#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import logging
import random
import telegram
from time import sleep

try:
  from urllib.error import URLError
except ImportError:
  from urllib2 import URLError

logging.basicConfig(filename='details.log',level=logging.WARNING)

def main():
  update_id = None

  try:
    os.environ['TELEGRAM_TOKEN']
  except:
    print 'You need the TELEGRAM_TOKEN variable'
    exit(1)

  bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])

  print 'Bot Telegram iniciado...'

  while True:
    try:
      update_id = checkMessages(bot, update_id)
    except telegram.TelegramError as e:
      if e.message in ("Bad Gateway", "Timed out"):
        sleep(1)
      else:
        raise e
    except URLError as e:
      sleep(1)


def checkMessages(bot, update_id):
# {
#   'message': {
#     'from': {
#       'first_name': u'Eduardo', 
#       'last_name': u'Schneiders', 
#       'id': 63458157
#     }, 
#     'text': u'testjng blaba', 
#     'chat': {
#       'first_name': u'Eduardo', 
#       'last_name': u'Schneiders', 
#       'type': u'private', 
#       'id': 63458157
#     }, 
#     'date': 1448645666, 
#     'message_id': 29
#   }, 
#   'update_id': 64440194
# }

    for update in bot.getUpdates(offset=update_id, timeout=10):
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        message = update.message.text
        logging.warning("Message: " + message)

        if message:

          if message == '/signup':
            bot.sendMessage(chat_id=chat_id, text='https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https://localhost/signup&client_id=' + os.environ['PINTEREST_CLIENT_ID'] + '&scope=read_public,write_public&state=' + str(chat_id))

    return update_id

if __name__ == '__main__':
  main()
