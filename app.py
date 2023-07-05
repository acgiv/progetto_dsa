from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
from Register import Client
import os

load_dotenv()

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
    rest = {"user_name": "", "email": "", "password": "",}
    client_register = Client(application=app, username=request.form.get("user_name"), email=request.form.get("email"),
                             password=request.form.get("password"),
                             confirm_password=request.form.get("confirm-password"),
                             genere=request.form.get("sex_type"),
                             date_birth=request.form.get("date_birth"))
    rest["user_name"], rest["email"], rest["password"] = client_register.control_user_email_password()
    return rest


if __name__ == '__main__':
    app.run(host='0.0.0.0')
