from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import request

import subprocess
from pi.gpio import set_output

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/gpio/', methods=['POST'])
def gpio():
    print(request.form);
    set_output(int(request.form['pin']), bool(request.form['value']))


@app.route('/cmd/', methods=['POST'])
def poster():
    cmd = request.form['cmd'].split(',')
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out, err = p.communicate()
    return out

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
