from flask import Flask, render_template, request, url_for, jsonify
import json
import requests


app = Flask(__name__)

@app.route('/')
def index():

  state = request.args.get('state')
  code = request.args.get('code')

  query_params = '?grant_type=authorization_code&client_id=client_id&client_secret=client_secret&code=' + code

  response = requests.post('https://api.pinterest.com/v1/oauth/token' + query_params)
  parsed_response =  json.loads(response.text)
  access_token = parsed_response['access_token']
  print(access_token)

  query_params = '?access_token=' + access_token + '&fields=id%2Clink%2Cnote%2Curl%2Cattribution%2Cmedia%2Cboard%2Coriginal_link%2Cmetadata%2Ccolor%2Ccounts%2Ccreated_at%2Ccreator%2Cimage'
  response = requests.get('https://api.pinterest.com/v1/me/pins' + query_params)
  parsed_response =  json.loads(response.text)

  for pin in parsed_response['data']:
    print(pin['image']['original']['url'])

  return response.text

@app.route('/test')
def test():
  return 'test'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000, debug=True)
