from __future__ import print_function

from flask import Flask
from flask import render_template
from flask import request
from flask import g

import subprocess
import pi.db as db
import pi.servo as servo

import xpibee
import webpigpio

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/xbee', methods=['POST'])
def xbeeSend():
    xpibee.send_transmit_request(request.form['addr'], request.form['data'])
    return 'xbee ok'


@app.route('/db')
def init_db():
    db.init_db(app)
    db.insert('settings', ('name', 'value'), ('light', 'on'))
    return 'db initialized'


@app.route('/gpio', methods=['POST'])
def gpio():
    return str(webpigpio.process_gpio_request(request.form))


@app.route('/servo', methods=['POST'])
def servo_position():
    return servo.position(request.form['sno'], request.form['angle'], request.form['delay'])


@app.route('/console', methods=['POST'])
def console():
    cmd = request.form['console'].split(',')
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out, err = p.communicate()
    return out


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0')

