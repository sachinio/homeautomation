from __future__ import print_function

import subprocess
import sys
import webpigpio
import xpibee

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
debug = False
if len(sys.argv) > 1:
    debug = sys.argv[1] == 'True'


@app.route('/')
def index():
    return render_template('garage.html')


@app.route('/xbee', methods=['POST'])
def xbee_send():
    xpibee.send_transmit_request(request.json['addr'], request.json['data'])
    return 'xbee ok'


@app.route('/gpio', methods=['POST'])
def gpio():
    return str(webpigpio.process_gpio_request(request.json))


#@app.route('/servo', methods=['POST'])
#def servo_position():
#    return servo.position(request.form['sno'], request.form['angle'], request.form['delay'])


@app.route('/console', methods=['POST'])
def console():
    cmd = request.json['console'].split(',')
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE,shell=True)
    out, err = p.communicate()
    print(out)
    print(err)
    return 'out: '+out + ' err: '+err;


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=debug)

