from __future__ import print_function

import json
import urllib2
import subprocess
import sys
import webpigpio
import picamera
import time
import serial
import socket
import requests

import datetime as dt

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import send_file
from pymongo import MongoClient

lastTime = 0

client = MongoClient()
db = client.home

app = Flask(__name__)
debug = False

cam = picamera.PiCamera()
cam.resolution = (1024,768)
cam.start_preview()

if len(sys.argv) > 1:
    debug = sys.argv[1] == 'True'

if len(sys.argv) > 2:
    db.android.insert_one({'key', sys.argv[2]})


def millis():
    return int(round(time.time() * 1000))


def chomp(x):
    if x.endswith("\r\n"): return x[:-2]
    if x.endswith("\n"): return x[:-1]
    return x[:]


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def xbee(idx, cmd, sync=False):
    ser = serial.Serial(port='/dev/ttyAMA0',baudrate=9600, timeout=3)
    ser.write(idx+'-'+cmd+'-')

    if sync:
        result = chomp(ser.readline())
        print(result)
        ser.close()
        return result
    ser.close()


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


def translate_ip(ip):
    if ip == '1':
        cam.rotation = 90
        return '10.0.0.19'
    if ip == '2':
        cam.rotation = 180
        return '10.0.0.20'


def get_camera(ip):
    if get_my_ip() != translate_ip(ip):
        return requests.get('http://'+translate_ip(ip)+':5000/camera?ip='+ip).content
    else:
        return camera_internal()


def camera_internal():
    filename = '/var/www/ram/campi.jpg'

    global lastTime

    if millis() - lastTime > 1000:
        cam.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cam.capture(filename, resize=(512, 288))
        lastTime = millis()
    else:
        print('returning old image')

    return send_file(filename, mimetype='image/jpeg')


@app.route('/camera')
def camera():
    ip = request.args.get('ip')
    return get_camera(ip)


@app.route('/device', methods=['POST'])
def device():
    idx = request.json['id']
    if idx == '1':
        cmd = None
        data = request.json['data']
        if data == '1':
            cmd = 'R,40,50,255,100,0,0'
        elif data == '0':
            cmd = 'O,40,50,255,100,0,0'
        xbee(idx, cmd)
        d = {'result': 'Laser ' + cmd}
    elif idx == '2':
        cmd = 'G,F,500,'
        xbee(idx, cmd)
        d = {'result': 'Garage'}
    elif idx == '3':
        cmd = 'D,F,500,'
        d = {'result': xbee(idx, cmd, True)}
    elif idx == '4':
        cmd = 'T,'
        d = {'result': xbee(idx, cmd, True)}
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

