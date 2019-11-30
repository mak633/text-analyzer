# encoding: utf-8

from flask import Flask, request, url_for, render_template
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

import json
import re
import sys

# enable import from same-level folders
sys.path.append('../')
from utils import preprocess, sentimenter
sys.modules['sentimenter'] = sentimenter

app = Flask(
  __name__,
  static_url_path='',
  static_folder='../client/dist/client',
  template_folder='../client/dist/client'
)

CORS(app)
api = Api(app)

@app.route('/')
def get():
  return render_template("index.html")

@app.route('/analize', methods=['POST'])
def analize():
  data = request.get_json()

  text = preprocess.clean_text(data['text'])
  sentiment = sentimenter.get_sentiment(text)

  result = {
    'clean_text': text,
    'sentiment': sentiment
  }

  return json.dumps({ 'result': result })
