#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import json
import requests

_PINTEREST_HOST = 'https://api.pinterest.com'

def my_boards(access_token):
  query_params = '?access_token=' + access_token + '&fields=id%2Cname%2Curl%2Ccreated_at%2Ccounts%2Ccreator%2Cdescription%2Cimage%2Cprivacy%2Creason'
  path = '/v1/me/following/boards/'
  response = requests.get(_PINTEREST_HOST + path + query_params)
  return json.loads(response.text)

def board_pins(board_id, access_token, next_page = ''):
  if next_page:
    endpoint = next_page
  else:
    query_params = '?access_token=' + access_token + '&fields=id%2Clink%2Cnote%2Curl%2Cimage&limit=2'
    path = '/v1/boards/' + board_id + '/pins/'
    endpoint = _PINTEREST_HOST + path + query_params

  response = requests.get(endpoint)
  return json.loads(response.text)

def my_pins(access_token):
  query_params = '?access_token=' + access_token + '&fields=id%2Clink%2Cnote%2Curl%2Cattribution%2Cmedia%2Cboard%2Coriginal_link%2Cmetadata%2Ccolor%2Ccounts%2Ccreated_at%2Ccreator%2Cimage'
  response = requests.get('https://api.pinterest.com/v1/me/pins' + query_params)
  return  json.loads(response.text)

  for pin in parsed_response['data']:
    img_url = pin['image']['original']['url']
    print('Sending photo: ' + img_url)
    bot.sendPhoto(chat_id=chat_id, photo=img_url)

