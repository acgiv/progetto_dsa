import functools
import requests
import openai
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import configparser
import os
from datetime import datetime

load_dotenv()
config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_KEY')
client = MongoClient(os.getenv('CONNECTION_DB'))
openai.api_key = os.getenv('TOKEN_CHAT_GPT')
app.db = client.dsa_application


def write_chatgpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
    print(response["choices"][0]["message"]["content"])
    return response["choices"][0]["message"]["content"]


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
                session["genere"] = lista[0]["sex_type"]
                return redirect(url_for("chat", session=True))
            else:
                return render_template('login.html', error_visible="",
                                       message_error=config["ERROR-MESSAGE"]['error_login'])
    return render_template('login.html', error_visible="d-none", message_error="", active_page='login',
                           session=(session.get("username") is not None))


def create_chat(id_chat, name_chat):
    date = datetime.today()
    session["id_message"] = 0
    new_collection = app.db[name_chat]
    new_collection.insert_one({
        "number_chat": id_chat,
        "title": "New chat",
        "message": [{
                     "id_message": 0,
                     'why': 'pepper',
                     'text': config['ROBOT-MESSAGE']['description-new_chat'],
                     'info_send_message': {"hour_minutes": date.strftime("%H:%M %p"),
                                           "Month_day": date.strftime("%b %d")}
                     }]
    })


def create_message_user(text, id_message, info_arrive_message):
    image_url = url_for('static', filename='image/png/user.png')
    message = f'''
     <div class="d-flex flex-row justify-content-end">
          <div>
               <p message_number="message_{id_message}" class="small p-2 me-3 mb-1 text-white rounded-3 mt-2 " style="background-color:#39ace7 ">
                 {text}
               </p>
               <p class="small me-3 mb-3 rounded-3 text-muted">{info_arrive_message['hour_minutes']} | {
                info_arrive_message['Month_day']}</p>
          </div>
          <img src="{image_url}" alt="avatar 1" style="width: 45px; height: 100%;">
      </div>
     '''
    return message


def create_message_robot(text, id_message, info_arrive_message):
    image_url = url_for('static', filename='image/png/pepper.png')
    message = f'''
     <div class="d-flex flex-row justify-content-start">
        <img src="{image_url}"
            alt="avatar=1" style="width: 45px; height: 100%;">
        <div class="d-flex flex-column">
            <div class="d-flex justify-content-between align-items-center">
                <p id="message_{id_message}" class="small p-2 ms-3 mb-1 rounded-3" style="background-color: #f5f6f7;">
                    {text}
                </p>
                <div>
                    <a onclick="send_message_text_pepper(\'message_{id_message}\')" class="ms-3"><i class="fas fa-robot chat_botton_send"></i></a>
                    <a onclick="reformulate_message(\'message_{id_message}\')" class="ms-3"><i class="fas fa-sync-alt chat_botton_send"></i></a>
                </div>
                </div>
                <div class="d-flex justify-content-end ">
                    <div class="me-5">
                        <p class="small ms-3 mb-3 rounded-3 text-muted ">{info_arrive_message['hour_minutes']
                        } | {info_arrive_message['Month_day']}</p>
                    </div>
                </div>
            </div>
        </div>
     '''
    return message


@app.route('/vew_chat', methods=['POST'])
def vew_chat(chat_number, title, message):
    image_url = url_for('static', filename='image/png/pepper.png')
    message = f'''
    <li class="p-2 border-bottom cursor_pointer">
        <a id="{chat_number}" class="d-flex justify-content-between text-decoration-none"
         onclick="view_chat_message(this)">
            <div class="d-flex flex-row">
                <div>
                    <img
                            src="{image_url}"
                            alt="avatar"
                            class="d-flex align-self-center me-4 pt-1"
                            width="50">
                
                </div>
                <div class="pt-2 p-2">
                    <p class="fw-bold mb-0 text-decoration-none">{title}</p>
                    <p class="small text-muted text-truncate chat_message d-inline-block">{message}</p>
                </div>
            </div>
        </a>
    </li>'''
    return message


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    username = session['username']
    content_view_chat = str()
    if f"{username}_chat" in app.db.list_collection_names():
        result = list(app.db[f"{username}_chat"].find())
        session["number_chat"] = result.__len__()
        for element in result:
            number_message = element["message"].__len__()
            content_view_chat += vew_chat(f"number_chat_{element['number_chat']}", element["title"],
                                          element["message"][number_message-1]["text"])
    else:
        session["number_chat"] = 0
    return render_template('chat.html', active_page='chat', session=True, content_view_chat=content_view_chat)


@app.route('/create_new_chat', methods=['GET', 'POST'])
@login_required
def create_new_chat():
    username = session['username']
    numbers_chat = session["number_chat"]
    session["number_chat"] = numbers_chat+1
    create_chat(numbers_chat, f"{username}_chat")
    chat_content = list(app.db[f"{username}_chat"].find({"number_chat": numbers_chat}))
    return vew_chat(f"number_chat_{numbers_chat}", chat_content[0]["title"],
                    chat_content[0]["message"][0]["text"])


@app.route('/view_chat_message', methods=['GET', 'POST'])
def view_chat_message():
    numbers = int(request.form.get("id_chat").replace("number_chat_", ""))
    username = session['username']
    content_message = str()
    result = list(app.db[f"{username}_chat"].find({"number_chat": numbers}))
    for message in result[0]["message"]:
        if message["why"].__eq__("pepper"):
            content_message += create_message_robot(message["text"], message["id_message"], message['info_send_message'])
        else:
            content_message += create_message_user(message["text"], message["id_message"], message['info_send_message'])
    return content_message


@app.route('/reformulate_message', methods=['GET', 'POST'])
def reformulate_message():
    date = datetime.today()
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    id_message = int(request.form.get("id_message").replace("message_", ""))
    info_send_message = {"hour_minutes": date.strftime("%H:%M %p"), "Month_day": date.strftime("%b %d")}
    result = list(app.db[f"{session['username']}_chat"].find({"number_chat": id_chat,
                                                              "message.id_message": id_message},
                                                             {'message.$': id_message-1}))[0]
    respost_chat_gpt = write_chatgpt(result['message'][0]["text"])
    update_message("pepper",
                 id_chat,
                 id_message,
                 f"{session['username']}_chat",
                   respost_chat_gpt,
                   info_send_message)
    return respost_chat_gpt

@app.route('/send_message_text_pepper', methods=['GET', 'POST'])
def send_message_text_pepper():
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    id_message = int(request.form.get("id_message").replace("message_", ""))
    result = list(app.db[f"{session['username']}_chat"].find({"number_chat": id_chat,
                                                              "message.id_message": id_message},
                                                             {'message.$': id_message}))[0]
    text = result['message'][0]["text"]
    server2_url = 'http://localhost:5001/'
    response = requests.post(server2_url, json={'message': text})
    print(response.text)
    return "true"


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


def update_message(why, id_chat, id_message, db_user_name, text,  info_arrive_message):
    elem = {"id_message": id_message,
            'why': why,
            'text': text,
            'info_send_message': info_arrive_message
            }
    app.db[db_user_name].update_one({'number_chat': id_chat}, {"$push": {"message": elem}})


@app.route('/send_message', methods=['POST'])
def send_message():
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    session["id_message"] += 1
    id_message = session["id_message"]
    date = datetime.today()
    info_send_message = {"hour_minutes": date.strftime("%H:%M %p"), "Month_day": date.strftime("%b %d")}
    update_message(session["username"],
                   id_chat,
                   id_message,
                   f"{session['username']}_chat",
                   request.form.get("chat_textarea"),
                   info_send_message)
    return create_message_user(request.form.get("chat_textarea"), id_message, info_send_message)


@app.route('/respost_message', methods=['POST'])
def response_message():
    date = datetime.today()
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    session["id_message"] += 1
    id_message = session["id_message"]
    info_send_message = {"hour_minutes": date.strftime("%H:%M %p"), "Month_day": date.strftime("%b %d")}
    respost_chat_gpt = write_chatgpt(request.form.get("chat_textarea"))
    update_message("pepper",
                   id_chat,
                   id_message,
                   f"{session['username']}_chat",
                   respost_chat_gpt,
                   info_send_message)
    return create_message_robot(respost_chat_gpt, id_message, info_send_message)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home', session=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
