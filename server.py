from flask import Flask, render_template, request, url_for, jsonify
import os
import json
import requests
import telegram

app = Flask(__name__)

@app.route('/')
def index():
  bot = telegram.Bot(os.environ['TELEGRAM_TOKEN'])
  chat_id = os.environ['TELEGRAM_CHAT_ID']
  client_id = os.environ['PINTEREST_CLIENT_ID']
  client_secret = os.environ['PINTEREST_CLIENT_SECRET']

  state = request.args.get('state')
  code = request.args.get('code')

  query_params = '?grant_type=authorization_code&client_id=' + client_id + '&client_secret=' + client_secret + '&code=' + code

  response = requests.post('https://api.pinterest.com/v1/oauth/token' + query_params)
  parsed_response =  json.loads(response.text)
  access_token = parsed_response['access_token']
  print(access_token)

  query_params = '?access_token=' + access_token + '&fields=id%2Clink%2Cnote%2Curl%2Cattribution%2Cmedia%2Cboard%2Coriginal_link%2Cmetadata%2Ccolor%2Ccounts%2Ccreated_at%2Ccreator%2Cimage'
  response = requests.get('https://api.pinterest.com/v1/me/pins' + query_params)
  parsed_response =  json.loads(response.text)

  for pin in parsed_response['data']:
    img_url = pin['image']['original']['url']
    print('Sending photo: ' + img_url)
    bot.sendPhoto(chat_id=chat_id, photo=img_url)

  query_params = '?access_token=' + access_token + '&fields=id%2Cname%2Curl%2Ccreated_at%2Ccounts%2Ccreator%2Cdescription%2Cimage%2Cprivacy%2Creason'
  response = requests.get('https://api.pinterest.com/v1/me/following/boards/' + query_params)
  parsed_response =  json.loads(response.text)

  print response.text
  for board in parsed_response['data']:
    query_params = '?access_token=' + access_token + '&fields=id%2Clink%2Cnote%2Curl%2Cimage'
    response = requests.get('https://api.pinterest.com/v1/boards/' + board['id'] + '/pins/' + query_params)
    parsed_response_board =  json.loads(response.text)

    pins = parsed_response_board['data']
    img_url = pins[0]['image']['original']['url']
    print('Sending photo: ' + img_url)
    bot.sendPhoto(chat_id=chat_id, photo=img_url)
    bot.sendMessage(chat_id=chat_id, text='Note: ' + pins[0]['note'])


  bot.sendMessage(chat_id=chat_id, text='Pomodoro')
  return response.text

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000, debug=True)
