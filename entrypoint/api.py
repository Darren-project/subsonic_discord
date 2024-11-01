import sys
sys.path.insert(0, '..')

from config import shared
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/api/appid')
def give_appid():
    return shared.d_app_cid

@app.route('/api/userid')
def give_userid():
    return shared.user_id

@app.route('/api/prevsong')
def give_prevsong():
        with open('../temp/prevsong.json', 'r') as file:
            prevsong = json.load(file)
        return jsonify(prevsong)