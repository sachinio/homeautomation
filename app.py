from __future__ import print_function

import json
import urllib2
import subprocess
import sys
import webpigpio
import xpibee

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from pymongo import MongoClient
client = MongoClient()
db = client.home

app = Flask(__name__)
debug = False
tokens = {}

if len(sys.argv) > 1:
    debug = sys.argv[1] == 'True'

if len(sys.argv) > 2:
    db.android.insert_one({'key', sys.argv[2]})


@app.route('/')
def index():
    return render_template('garage.html')


@app.route('/register', methods=['POST'])
def register():
    tokens[request.json['token']] = True
    print(tokens.keys())
    d = {'result': 'ok'}
    return jsonify(**d)


@app.route('/notify', methods=['POST'])
def notify():
    title = request.json['title']
    text = request.json['text']
    cursor = db.android.find()
    print(cursor[0])
    key = cursor[0]['key']
    print(key)

    d = {'result': 'ok'}
    return jsonify(**d)

    for t in tokens:
        data = {"notification": { "title": title, "text": text}, "to": t}

        req = urllib2.Request('https://gcm-http.googleapis.com/gcm/send')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', key)
        urllib2.urlopen(req, json.dumps(data))

    d = {'result': 'ok'}
    return jsonify(**d)


@app.route('/xbee', methods=['POST'])
def xbee_send():
    xpibee.send_transmit_request(request.json['addr'], request.json['data'])
    d = {'result': 'ok'}
    return jsonify(**d)


@app.route('/xbee2', methods=['POST'])
def xbee2_send():
    d = {'result': xpibee.send_transmit_request(request.json['addr'], request.json['data'], True)[2]}
    return jsonify(**d)


@app.route('/gpio', methods=['POST'])
def gpio():
    d = {'result': str(webpigpio.process_gpio_request(request.json))}
    return jsonify(**d)


#@app.route('/servo', methods=['POST'])
#def servo_position():
#    return servo.position(request.form['sno'], request.form['angle'], request.form['delay'])


@app.route('/console', methods=['POST'])
def console():
    cmd = request.json['console'].split(',')
    print(request.json)
    print(cmd)
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)

    if 'async' not in request.json.keys() or request.json['async'] == 'False':
            print('Running in sync')
            out, err = p.communicate()
            return 'out: ' + out + '\nerr: '+err

    print('Running Async')
    return "started command async"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=debug)

