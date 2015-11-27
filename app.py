from __future__ import print_function
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test/', methods=['POST'])
def poster():
    print(request.form)
    return 'Got it'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')