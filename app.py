import functools
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import configparser
import os

load_dotenv()
config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_KEY')
client = MongoClient(os.getenv('CONNECTION_DB'))
app.db = client.dsa_application


def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for(".login"))
        return route(*args, **kwargs)

    return route_wrapper


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('layout.html', active_page='home', session=(session.get("username") is not None))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get("user_name") is not None:
            lista = list(app.db.utenti.find({"user_name": request.form.get("user_name")}))
            if len(lista).__eq__(1) and pbkdf2_sha256.verify(request.form.get("password"), lista[0]["password"]):
                session["username"] = request.form.get("user_name")
                return redirect(url_for("chat", session=True))
            else:
                return render_template('login.html', error_visible="",
                                       message_error=config["ERROR-MESSAGE"]['error_login'])
    return render_template('login.html', error_visible="d-none", message_error="", active_page='login',
                           session=(session.get("username") is not None))


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return render_template('chat.html', active_page='chat', session=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = {"user_name": request.form.get("user_name"),
                    "email": request.form.get("email"),
                    "password": pbkdf2_sha256.hash(request.form.get("password")),
                    "sex_type": request.form.get('inlineRadioOptions'),
                    "date_birth": request.form.get("date_birth")}
        app.db.utenti.insert_one(new_user)
        return redirect(url_for('login'))
    return render_template('register.html', active_page='register', session=(session.get("username") is not None))


@app.route('/verifier', methods=['POST'])
def verifier_text():
    rest = {"user_name": False, "email": False, "password": ""}
    if request.form.get("user_name") is not None:
        lista = list(app.db.utenti.find({"user_name": request.form.get("user_name")}))
        if not len(lista).__eq__(0):
            rest.update(user_name=config["ERROR-MESSAGE"]['error_user_name'])
    if request.form.get("email") is not None:
        lista = list(app.db.utenti.find({"email": request.form.get("email")}))
        if not len(lista).__eq__(0):
            rest.update(email=config["ERROR-MESSAGE"]['error_email'])
    if not request.form.get("password").__eq__(request.form.get("confirm-password")):
        rest.update(password=config["ERROR-MESSAGE"]['error_equal_password'])

    return rest


@app.route('/create_new_chat', methods=['POST'])
def create_message():
    message = '''<li class="p-2 border-bottom">
                                            <a href="#!" class="d-flex justify-content-between text-decoration-none">
                                                <div class="d-flex flex-row">
                                                    <div>
                                                        <img
                                                                src='https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava1-bg.webp'
                                                                alt="avatar"
                                                                class="d-flex align-self-center me-4 pt-1"
                                                                width="50">
                                                        <span class="badge bg-success badge-dot"></span>
                                                    </div>
                                                    <div class="pt-2 p-2">
                                                        <p class="fw-bold mb-0 text-decoration-none">New chat</p>
                                                        <p class="small text-muted text-truncate chat_message d-inline-block">Hello, Are you theressssssssssssssssssssssssssssssssssssssssssssss?</p>
                                                    </div>
                                                </div>
                                            </a>
                                        </li>'''
    return message


@app.route('/send_message', methods=['POST'])
def send_message():
    message = '''<div id="message_robot" class="d-flex flex-row justify-content-start">
                                   
                                    <div>
                                        <p id="message" class="  small p-2 ms-3 mb-1 rounded-3"
                                           style="background-color: #f5f6f7;">
                                            magna aliqua. sono qui.</p> 
                                        <p class="small ms-3 mb-3 rounded-3 text-muted float-end">12:00 PM | Aug
                                            13</p>
                                    </div>
                                </div>'''
    return message


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home', session=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
