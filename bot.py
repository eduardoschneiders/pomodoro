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
from redis import Redis
from rq import Queue

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

    for update in bot.getUpdates(offset=update_id, timeout=60):
        chat_id = update.message.chat_id
        update_id = update.update_id + 1

        message = update.message.text
        logging.warning("Message: " + message)

        if message:

          if message == '/signup':
            bot.sendMessage(chat_id=chat_id, text='https://api.pinterest.com/oauth/?response_type=code&redirect_uri=https://localhost/signup&client_id=' + os.environ['PINTEREST_CLIENT_ID'] + '&scope=read_public,write_public,read_relationships,write_relationships&state=' + str(chat_id))

          if message == '/start':
            start(bot, chat_id)

    return update_id

def user(chat_id):
  db_connection = sqlite.connect('pomodoro.db')
  db_curs = db_connection.cursor()
  db_curs.execute('SELECT * FROM users where chat_id = ' + str(chat_id))
  user = db_curs.fetchone()
  return user

def send_content(bot, chat_id, access_token):
  global pinterest_client
  import pinterest_client
  q = Queue(connection=Redis())

  db_connection = sqlite.connect('pomodoro.db')
  db_curs = db_connection.cursor()

  boards = pinterest_client.my_boards(access_token)

  for board in boards['data']:
    db_curs.execute('SELECT next_page FROM boards where name = "' + board['name'] + '"')
    board_db = db_curs.fetchone()
    next_page = board_db[0] if board_db else None

    pins = pinterest_client.board_pins(board['id'], access_token, next_page)

    for pin in pins['data']:
      print board['name'] + ': ' + pin['note']
      print pin['image']['original']['url']

      result = q.enqueue(bot.sendPhoto, chat_id=chat_id, photo=pin['image']['original']['url'])
      result = q.enqueue(bot.sendMessage, chat_id=chat_id, text=board['name'] + ': ' + pin['note'])

    if board_db:
      db_curs.execute('UPDATE boards SET next_page = "' + pins['page']['next'] + '" WHERE name = "' + board['name'] + '"')
    else:
      db_curs.execute('INSERT INTO boards (name, next_page) VALUES ("' + board['name'] + '", "' + pins['page']['next'] + '")')
    db_connection.commit()

def start(bot, chat_id):
  text = 'Start working'
  print text
  bot.sendMessage(chat_id, text=text)
  threading.Timer(25*60.0, rest, [bot, chat_id]).start()

def rest(bot, chat_id):
  text = 'Now you can rest'
  print text
  bot.sendMessage(chat_id, text=text)

  current_user = user(chat_id)
  send_content(bot, chat_id, current_user[5])
  threading.Timer(5*60.0, start, [bot, chat_id]).start()

if __name__ == '__main__':
  main()
