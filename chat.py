from datetime import datetime
from flask import url_for


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
            button += f'<a onclick="send_message_text_pepper(\'{id_message}\')" class="ms-3"><i class="fas ' \
                      f'fa-robot chat_botton_send"></i></a>' \
                      f'<a onclick="reformulate_message(\'{id_message}\')" class="ms-3"><i class="fas ' \
                      f'fa-sync-alt chat_botton_send"></i></a>'
            if not self.number_id_max_text(id_chat, id_message).__eq__(0):
                visible = ""
                position = f'{id_text + 1}/{self.number_text_message_generate(id_chat, id_message)}'
            button_next = f'<a id="back_{id_message}" onclick="goToBack(\'{id_message}\')" class="ms-3 ' \
                          f'{visible}"><i class="fas ' \
                          f'fa-chevron-left chat_botton_send"></i></a><span id="text_{id_message}" class="ms-2 ' \
                          f'{visible}">{position}</span>' \
                          f'<a id="next_{id_message}" onclick="goToNext(\'{id_message}\')" class="ms-2 {visible}"><i ' \
                          f'class="fas fa-chevron-right chat_botton_send"></i></a>'
        message = f'''
            <div class="d-flex flex-row justify-content-start">
                <img src="{image_url}" alt="avatar=1" style="width: 45px; height: 100%;">
                <div class="d-flex flex-column">
                    <div class="d-flex justify-content-between align-items-center">
                        <p id="message_{id_message}" id_text="{id_text}" class="small p-2 ms-3 mb-1 rounded-3" 
                        style="background-color: #f5f6f7;"> {text[id_text]}
                        </p>
                    </div>
                    <div class="d-flex bd-highlight mb-3">
                        <div class="p-2 bd-highlight">
                            <div class="ms-3">  
                                {button_next}
                                {button}
                            </div>
                        </div>
                        <div class="ms-auto p-2 bd-highlight">
                            <div class="me-5">
                                <p id="info_{id_message}" class="small ms-3 mb-3 rounded-3 text-muted">
                                    {info_arrive_message['hour_minutes']} | {info_arrive_message['Month_day']}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
         '''
        return message

    @staticmethod
    def create_message_user(text, id_message, info_arrive_message):
        image_url = url_for('static', filename='image/png/user.png')
        message = f'''
         <div class="d-flex flex-row justify-content-end">
              <div>
                   <p message_number="message_{id_message}" class="small p-2 me-3 mb-1 text-white rounded-3 mt-2 " 
                   style="background-color:#39ace7 "> {text}
                   </p>
                   <p class="small me-3 mb-3 rounded-3 text-muted">{info_arrive_message['hour_minutes']} | {
        info_arrive_message['Month_day']}</p>
              </div>
              <img src="{image_url}" alt="avatar 1" style="width: 45px; height: 100%;">
          </div>
         '''
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

