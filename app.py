from __future__ import print_function
from subprocess import Popen
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test/', methods=['POST'])
def poster():
    return Popen(["request.form['cmd']", ""], stdout=PIPE).communicate()[0]

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
