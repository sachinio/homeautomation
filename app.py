from __future__ import print_function
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test/', methods=['POST'])
def poster():
    cmd = ["sudo",request.form['cmd']]
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.PIPE)
    out,err = p.communicate()
    return out

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
