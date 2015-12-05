from __future__ import print_function

import subprocess

import webpigpio
import xpibee
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/xbee', methods=['POST'])
def xbeeSend():
    print(request.form)
    xpibee.send_transmit_request(request.form['addr'], request.form['data'])
    return 'xbee ok'


@app.route('/gpio', methods=['POST'])
def gpio():
    return str(webpigpio.process_gpio_request(request.form))


#@app.route('/servo', methods=['POST'])
#def servo_position():
#    return servo.position(request.form['sno'], request.form['angle'], request.form['delay'])


@app.route('/console', methods=['POST'])
def console():
    cmd = request.form['console'].split(',')
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out, err = p.communicate()
    return out


if __name__ == '__main__':
    app.run(host='0.0.0.0')

