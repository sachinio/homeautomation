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

if len(sys.argv) > 1:
    debug = sys.argv[1] == 'True'

if len(sys.argv) > 2:
    db.android.insert_one({'key', sys.argv[2]})


@app.route('/')
def index():
    return render_template('garage.html')


@app.route('/register', methods=['POST'])
def register():
    db.gcmtokens.update({'token': request.json['token']},{'token': request.json['token']}, upsert=True)
    d = {'result': 'ok'}
    return jsonify(**d)


@app.route('/notify', methods=['POST'])
def notify():
    title = request.json['title']
    text = request.json['text']

    c = db.android.find()
    key = None
    for d in c:
        if 'auth' in d.keys():
            key = d['auth']

    if key is None:
        print("Invalid Key")
        d = {'result': 'not ok'}
        return jsonify(**d)

    for t in db.gcmtokens.find():
        data = {"notification": { "title": title, "text": text}, "to": t['token']}
        print(data)

        req = urllib2.Request('https://gcm-http.googleapis.com/gcm/send')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', key)
        urllib2.urlopen(req, json.dumps(data))

    d = {'result': 'ok'}
    return jsonify(**d)


@app.route('/device', methods=['POST'])
def device():
    id = request.json['id']
    if id == '1':
        cmd = ",40,50,255,100,0,0"
        data = request.json['data']
        if data == '1':
            cmd = 'R' + cmd
        elif data == '0':
            cmd = 'O' + cmd
        xpibee.send_transmit_request("00 13 A2 00 40 BF 8A C8", cmd)
        d = {'result': 'Laser ' + cmd}
    elif id == '2':
        cmd = 'G,F,500,'
        xpibee.send_transmit_request("00 13 A2 00 40 BF 8E 93", cmd)
        d = {'result': 'Garage'}
    elif id == '3':
        cmd = 'D,F,500,'
        d = {'result': xpibee.send_transmit_request("00 13 A2 00 40 BF 8E 93", cmd, True)[2]}
    elif id == '4':
        cmd = 'T,'
        d = {'result': xpibee.send_transmit_request("00 13 A2 00 40 BF 8E 7B", cmd, True)[2]}
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

