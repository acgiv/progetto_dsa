from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import hashlib
import configparser
import datetime
import os

load_dotenv()
config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")

app = Flask(__name__)
client = MongoClient(os.getenv('CONNECTION_DB'))
app.db = client.dsa_application

testo_list = []


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get("user_name") is not None:
            h = hashlib.new('sha256')
            h.update(request.form.get("password").encode())
            print(request.form.get("user_name"), request.form.get("password"))
            lista = list(app.db.utenti.find({"user_name": request.form.get("user_name"), "password": h.hexdigest()}))
            if len(lista).__eq__(1):
                return render_template("chat.html")
            else:
                return render_template('login.html')
    return render_template('login.html')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template("chat.html",
                           format_data=datetime.datetime.today().strftime("%d %H:%M:%S"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        h = hashlib.new('sha256')
        h.update(request.form.get("password").encode())
        new_user = {"user_name": request.form.get("user_name"),
                    "email": request.form.get("email"),
                    "password": h.hexdigest(),
                    "sex_type": request.form.get('inlineRadioOptions'),
                    "date_birth": request.form.get("date_birth")}
        app.db.utenti.insert_one(new_user)
        return render_template('login.html')
    return render_template('register.html')


@ app.route('/verifier', methods=['POST'])
def verifier_text():
    rest = {"user_name": False, "email": False, "password": ""}

    if request.form.get("user_name") is not None:
        lista = list(app.db.utenti.find({"username": request.form.get("user_name")}))
        if not len(lista).__eq__(0):
            rest.update(user_name=config["ERROR-MESSAGE"]['error_user_name'])

    if request.form.get("email") is not None:
        lista = list(app.db.utenti.find({"email": request.form.get("email")}))
        if not len(lista).__eq__(0):
            rest.update(email=config["ERROR-MESSAGE"]['error_email'])

    if not request.form.get("password").__eq__(request.form.get("confirm-password")):
        rest.update(password=config["ERROR-MESSAGE"]['error_equal_password'])

    return rest


if __name__ == '__main__':
    app.run(host='0.0.0.0')
