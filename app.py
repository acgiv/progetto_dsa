from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
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
def chat():
    # print([e for e in app.db.utenti.find({})])
    if request.method == 'POST':
        testo = request.form['testo']
        if not len(testo.strip()).__eq__(0):
            testo_list.append(testo)
    return render_template("chat.html", testo_list=testo_list,
                           format_data=datetime.datetime.today().strftime("%d %H:%M:%S"))


# Pagina di accesso
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome_utente = request.form["user_name"]
        password = request.form['password']
        app.db.utenti.insert_one({"username": nome_utente, "password": password})
        return render_template("chat.html")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


@app.route('/verifier', methods=['POST'])
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
