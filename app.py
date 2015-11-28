from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import request
from flask import g

from pi.gpio import process_gpio_request

import subprocess
import pi.db


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/db')
def init_db():
    pi.db.init_db(app)
    pi.db.insert('settings', ('name', 'value'), ('light', 'on'))
    return 'db initialized'


@app.route('/gpio', methods=['POST'])
def gpio():
    process_gpio_request(request.form)
    return 'ok'


@app.route('/cmd', methods=['POST'])
def poster():
    cmd = request.form['cmd'].split(',')
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
    app.run(debug=True, host='0.0.0.0')

