from flask import Blueprint, render_template


app = Blueprint("main", __name__)


@app.route('/')
def index():
    return render_template('index/index.html', title="home")


@app.route('/login')
def login():
    return render_template('login/login.html', title="登录")
