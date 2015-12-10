#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import logging
import random
import telegram
from time import sleep
import threading
from sqlite3 import dbapi2 as sqlite
import json

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

          if message == '/start':
            start(bot, chat_id)

    return update_id

def user(chat_id):
  db_connection = sqlite.connect('pomodoro.db')
  db_curs = db_connection.cursor()
  db_curs.execute('SELECT * FROM users')
  user = db_curs.fetchone()
  return user

def send_content(bot, chat_id, access_token):
  global requests
  import requests
  global json
  import json

  query_params = '?access_token=' + access_token + '&fields=id%2Clink%2Cnote%2Curl%2Cattribution%2Cmedia%2Cboard%2Coriginal_link%2Cmetadata%2Ccolor%2Ccounts%2Ccreated_at%2Ccreator%2Cimage'
  response = requests.get('https://api.pinterest.com/v1/me/pins' + query_params)
  parsed_response =  json.loads(response.text)

  for pin in parsed_response['data']:
    img_url = pin['image']['original']['url']
    print('Sending photo: ' + img_url)
    bot.sendPhoto(chat_id=chat_id, photo=img_url)

def start(bot, chat_id):
  text = 'Start working'
  print text
  bot.sendMessage(chat_id, text=text)
  threading.Timer(5.0, rest, [bot, chat_id]).start()

def rest(bot, chat_id):
  text = 'Now you can rest'
  print text
  bot.sendMessage(chat_id, text=text)

  current_user = user(chat_id)
  send_content(bot, chat_id, current_user[5])
  threading.Timer(180.0, start, [bot, chat_id]).start()

if __name__ == '__main__':
  main()
