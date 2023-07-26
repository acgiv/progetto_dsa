import configparser
from datetime import datetime
from flask import url_for

config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")


class Chat:
    def __init__(self, app, session, text_file):
        self.app = app
        self.session = session
        self.text_file = text_file

    def number_text_message_generate(self, id_chat, id_message):
        return self.app.db[f"{self.session['username']}_chat"].find({'number_chat': id_chat,
                                                                     'message.id_message': id_message}
                                                                    )[0]["message"][id_message]["text"].__len__()

    def create_chat(self, id_chat, name_chat):
        date = datetime.today()
        self.session["id_message"] = 0
        new_collection = self.app.db[name_chat]
        new_collection.insert_one({
            "number_chat": id_chat,
            "title": "New chat",
            "message": [{
                "id_message": 0,
                "id_text": 0,
                'why': 'pepper',
                'text': [self.text_file['ROBOT-MESSAGE']['description-new_chat']],
                'info_send_message': {"hour_minutes": date.strftime("%H:%M %p"),
                                      "Month_day": date.strftime("%b %d")}
            }]
        })

    def create_message_robot(self, text, id_chat, id_message, id_text, info_arrive_message):
        image_url = url_for('static', filename='image/png/pepper.png')
        button, button_next, visible, position = "", "", "d-none", ""
        if not id_message.__eq__(0):
            button += config["CHAT"]["button_robot"].format(id_message, id_message)
            if not self.number_id_max_text(id_chat, id_message).__eq__(0):
                visible = ""
                position = f'{id_text + 1}/{self.number_text_message_generate(id_chat, id_message)}'
            button_next = config["CHAT"]["button_next_robot"].format(id_message, id_message, visible, id_message,
                                                                     visible, position, id_message, id_message, visible)
        return config["CHAT"]["message_robot"].format(image_url, id_message, id_text, text[id_text], button_next, button,
                                                      id_message, info_arrive_message['hour_minutes'],
                                                      info_arrive_message['Month_day'])


    @staticmethod
    def create_message_user(text, id_message, info_arrive_message):
        image_url = url_for('static', filename='image/png/user.png')
        message = config["CHAT"]["message_user"].format(id_message, text, info_arrive_message['hour_minutes'],
                                                        info_arrive_message['Month_day'], image_url)
        return message

    def update_message_user(self, why, id_chat, id_message, db_user_name, text, info_arrive_message):
        elem = {"id_message": id_message,
                'why': why,
                'text': text,
                'info_send_message': info_arrive_message
                }
        self.app.db[db_user_name].update_one({'number_chat': id_chat}, {"$push": {"message": elem}})

    def set_position_text(self, id_chat, id_message, id_text):
        self.app.db[f"{self.session['username']}_chat"].update_one(
            {
                "number_chat": id_chat,
                "message.id_message": id_message
            },
            {
                "$set": {
                    "message.$.id_text": id_text,
                }
            }
        )

    def set_title(self, id_chat, id_title):
        self.app.db[f"{self.session['username']}_chat"].update_one(
            {
                "number_chat": id_chat,
            },
            {
                "$set": {
                    "title": id_title,
                }
            }
        )

    def search_message(self, id_chat, id_message):
        return list(self.app.db[f"{self.session['username']}_chat"]
                    .find({"number_chat": id_chat,
                           "message.id_message": id_message},
                          {"message": {"$elemMatch": {"id_message": id_message}}}))[0]

    def number_id_max_text(self, id_chat, id_message):
        return self.app.db[f"{self.session['username']}_chat"].find({'number_chat': id_chat,
                                                                     'message.id_message': id_message}
                                                                    )[0]["message"][id_message]["text"].__len__()

    def get_last_id_message(self, id_chat):
        return self.app.db[f"{self.session['username']}_chat"].find(
            {'number_chat': id_chat})[0]["message"][-1]["id_message"]

    @staticmethod
    def get_type_person(eta):
        if eta <= 10:
            return "bambino"
        elif eta < 30:
            return "ragazzo"
        elif eta < 70:
            return "persona"
        else:
            return "anziano"
