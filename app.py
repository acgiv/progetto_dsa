import functools
import requests
import openai
from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
from passlib.hash import pbkdf2_sha256
import configparser
import os
from datetime import datetime
from chat import Chat

load_dotenv()
config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")

app = Flask(__name__)
app.secret_key = os.getenv('SESSION_KEY')
client = MongoClient(os.getenv('CONNECTION_DB'))
openai.api_key = os.getenv('TOKEN_CHAT_GPT')
app.db = client.dsa_application
app.chat = Chat(app, session, config)


def write_chatgpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
    )
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
                                          element["message"][number_message-1]["text"][0])
    else:
        session["number_chat"] = 0
    return render_template('chat.html', active_page='chat', session=True, content_view_chat=content_view_chat)


@app.route('/create_new_chat', methods=['GET', 'POST'])
@login_required
def create_new_chat():
    username = session['username']
    numbers_chat = session["number_chat"]
    session["number_chat"] = numbers_chat+1
    app.chat.create_chat(numbers_chat, f"{username}_chat")
    chat_content = list(app.db[f"{username}_chat"].find({"number_chat": numbers_chat}))
    return vew_chat(f"number_chat_{numbers_chat}", chat_content[0]["title"],
                    chat_content[0]["message"][0]["text"][0])


@app.route('/view_chat_message', methods=['GET', 'POST'])
def view_chat_message():
    numbers = int(request.form.get("id_chat").replace("number_chat_", ""))
    username = session['username']
    content_message = str()
    result = list(app.db[f"{username}_chat"].find({"number_chat": numbers}))
    for message in result[0]["message"]:
        if message["why"].__eq__("pepper"):
            content_message += app.chat.create_message_robot(message["text"], numbers, message["id_message"],
                                                             message["id_text"], message['info_send_message'])
        else:
            content_message += app.chat.create_message_user(message["text"], message["id_message"],
                                                            message['info_send_message'])
    return content_message


@app.route('/reformulate_message', methods=['GET', 'POST'])
def reformulate_message():
    date = datetime.today()
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    id_message = int(request.form.get("id_message").replace("message_", ""))
    info_send_message = {"hour_minutes": date.strftime("Modified %H:%M %p"), "Month_day": date.strftime("%b %d")}
    result = app.chat.search_message(id_chat, id_message-1)
    new_id_text = app.chat.number_id_max_text(id_chat, id_message)
    respost_chat_gpt = write_chatgpt(result["message"][0]["text"])
    app.db[f"{session['username']}_chat"].update_one(
        {
            "number_chat": id_chat,
            "message.id_message": id_message
        },
        {
            "$set": {
                "message.$.id_text": new_id_text,
                "message.$.info_send_message": info_send_message
            },
            "$push": {
                "message.$.text": respost_chat_gpt
            }
        }
    )

    return {"message": respost_chat_gpt, "id_text": new_id_text, "info_message": info_send_message}


@app.route('/send_message_text_pepper', methods=['GET', 'POST'])
def send_message_text_pepper():
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    id_message = int(request.form.get("id_message").replace("message_", ""))
    id_text = int(request.form.get("id_text"))
    result = app.chat.search_message(id_chat, id_message)
    text = result["message"][0]["text"][id_text]
    server2_url = 'http://localhost:5001/'
    return str(requests.post(server2_url, json={'message': text}).text)


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


@app.route('/send_message', methods=['POST'])
def send_message():
    session["id_message"] += 1
    id_message = session["id_message"]
    ed_elem = request.form.get("id_chat").replace("number_chat_", "").split("_")
    id_chat = int(ed_elem[0])
    date = datetime.today()
    info_send_message = {"hour_minutes": date.strftime("%H:%M %p"), "Month_day": date.strftime("%b %d")}
    app.chat.update_message_user(session["username"], id_chat, id_message, f"{session['username']}_chat",
                                 request.form.get("chat_textarea"), info_send_message)
    return app.chat.create_message_user(request.form.get("chat_textarea"), id_message, info_send_message)


@app.route('/respost_message', methods=['POST'])
def response_message():
    date = datetime.today()
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    id_text = 0
    session["id_message"] += 1
    info_send_message = {"hour_minutes": date.strftime("%H:%M %p"), "Month_day": date.strftime("%b %d")}
    respost_chat_gpt = [write_chatgpt(request.form.get("chat_textarea"))]
    elem = {"id_message": session["id_message"],
            "id_text": id_text,
            'why': "pepper",
            'text': respost_chat_gpt,
            'info_send_message': info_send_message
            }
    app.db[f"{session['username']}_chat"].update_one({'number_chat': id_chat}, {"$push": {"message": elem}})
    return app.chat.create_message_robot(respost_chat_gpt, id_chat, session["id_message"], id_text, info_send_message)


@app.route('/goToBack', methods=['POST'])
def goToBack():
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    id_message = int(request.form.get("id_message").replace("message_", ""))
    id_text = int(request.form.get("id_text"))
    if id_text > 0:
        result = app.chat.search_message(id_chat, id_message)
        max_len_id = result["message"][0]["text"].__len__()
        app.chat.set_position_text(id_chat, id_message, id_text-1)
        return {"on": True, "message": result["message"][0]["text"][id_text-1], "id_text": id_text-1,
                "position_id_text": id_text, "id_max_text": max_len_id}
    else:
        return {"on": False}


@app.route('/goToNext', methods=['POST'])
def goToNext():
    id_message = int(request.form.get("id_message").replace("message_", ""))
    id_chat = int(request.form.get("id_chat").replace("number_chat_", ""))
    result = app.chat.search_message(id_chat, id_message)
    max_len_id = result["message"][0]["text"].__len__()
    id_text = int(request.form.get("id_text"))+1
    if id_text < max_len_id:

        app.chat.set_position_text(id_chat, id_message, id_text)
        return {"on": True, "message": result["message"][0]["text"][id_text], "id_text": id_text,
                "position_id_text": id_text+1, "id_max_text": max_len_id}
    else:
        return {"on": False}


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home', session=False))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
