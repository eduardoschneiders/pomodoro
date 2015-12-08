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
  return response.text + state + code

@app.route('/test')
def test():
  return 'test'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000, debug=True)
