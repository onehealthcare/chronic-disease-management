import os
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return f'Hello World!{os.getpid()}'


@app.route('/ping')
def ping():
    return 'ok'


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)
