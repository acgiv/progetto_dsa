import configparser
from datetime import datetime

from flask_wtf import FlaskForm
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, InputRequired, ValidationError

config = configparser.ConfigParser()
config.read(".\\config\\gobal_variable.ini")


class LoginForm(FlaskForm):
    def __init__(self, app, session, **kwargs):
        super().__init__(**kwargs)
        self.result_search, self.user = None, None
        self.app = app
        self.session = session

    def check_username(self, field):
        self.result_search = list(self.app.db.utenti.find({"user_name": field.data}))
        self.user = field.data

    def check_password(self, field):
        print(len(self.result_search))
        if len(self.result_search) == 0 or not pbkdf2_sha256.verify(field.data, self.result_search[0]["password"]):
            raise ValidationError(config["ERROR-MESSAGE"]["error_login"])
        else:
            self.session["username"] = self.user
            self.session["date"] = datetime.now().year - int(self.result_search[0]["date_birth"].split("-")[0])

    username = StringField("Username", validators=[InputRequired(), check_username, Length(min=3)])
    password = PasswordField("Password", validators=[InputRequired(), check_password, Length(min=3)])
    login = SubmitField("Login")
