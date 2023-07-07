from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import configparser
import datetime
import os

load_dotenv()
config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_KEY')
client = MongoClient(os.getenv('CONNECTION_DB'))
app.db = client.dsa_application

testo_list = []


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('layout.html', active_page='home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get("user_name") is not None:
            print(request.form.get("user_name"), pbkdf2_sha256.hash(request.form.get("password")))
            lista = list(app.db.utenti.find({"user_name": request.form.get("user_name")}))
            if len(lista).__eq__(1) and pbkdf2_sha256.verify(request.form.get("password"), lista[0]["password"]):
                return redirect(url_for("chat"))
            else:
                return render_template('login.html', error_visible="",
                                       message_error=config["ERROR-MESSAGE"]['error_login'])
    return render_template('login.html', error_visible="d-none", message_error="",  active_page='login')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('chat.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = {"user_name": request.form.get("user_name"),
                    "email": request.form.get("email"),
                    "password": pbkdf2_sha256.hash(request.form.get("password")),
                    "sex_type": request.form.get('inlineRadioOptions'),
                    "date_birth": request.form.get("date_birth")}
        app.db.utenti.insert_one(new_user)
        session["user"] = request.form.get("user_name")
        return redirect(url_for('login'))
    return render_template('register.html', active_page='register')


@ app.route('/verifier', methods=['POST'])
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


@app.route('/logout')
def logout():
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
