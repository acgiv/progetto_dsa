from pymongo import MongoClient
import os
import configparser
import gladiator as gl

config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")


class Client:
    def __init__(self, application, username, email, password, confirm_password,
                 genere=None, date_birth=None):
        self.app = application
        self.__connection_db()
        self.username = username
        self.email = email
        self.password = password
        self.conf_passowrd = confirm_password
        self.genere = genere
        self.data_nascita = date_birth

    def __connection_db(self):
        client = MongoClient(os.getenv('CONNECTION_DB'))
        self.db = client.dsa_application

    def control_user(self):
        if self.username is not None:
            lista = list(self.app.db.utenti.find({"username": self.username}))
            if not len(lista).__eq__(0):
                return config["ERROR-MESSAGE"]['error_user_name']
            else:
                return False

    def control_email(self):
        lista = list(self.app.db.utenti.find({"email": self.email}))
        if not len(lista).__eq__(0):
            return config["ERROR-MESSAGE"]['error_email']
        else:
            return False

    def control_password(self):
        if self.password.__eq__(self.conf_passowrd):
            return ""
        else:
            return config["ERROR-MESSAGE"]['error_equal_password']

    def control_user_email_password(self):
        return self.control_user(), self.control_email(), self.control_password()

    def get_client(self):
        return {"user_name": self.username,
                "email": self.email,
                "password": self.password,
                "conf_password": self.conf_passowrd,
                "sex_type": self.genere,
                "date_birth": self.data_nascita,
                "botton_crea": False
                }