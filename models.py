from data import db_session
from data import Articles
from data import Comments
from data import Users
import os
import sqlite3
import flask
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
DATABASE_URL = r"C:\Users\Alexey\PycharmProjects\guest_book\oh_no.db"
db_session.global_init(DATABASE_URL)
'''
class Article:
    def __init__(self, article_id, title, content, comments):
        self.id = article_id
        self.title = title
        self.content = content
        self.comments = comments

    def get_title(self):
        return self.title

    def get_content(self):
        return self.content

    def get_comments(self):
        return self.comments

    def get_id(self):
        return self.id


class Comment:
    def __init__(self, comment_id, author, content):
        self.id = comment_id
        self.author = author
        self.content = content

    def get_author(self):
        return self.author

    def get_content(self):
        return self.content

    def get_id(self):
        return self.id
    
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.login = User.get_login(self)
        self.password = User.get_password(self)

    def get_login(self):
        session = db_session.create_session()
        return session.query(Users.Users).filter(Users.Users.id == self.id).one().login
        return cur.execute(SELECT login FROM Users
                        WHERE id = ?, (self.id,)).fetchone()[0]

    def get_password(self):
        session = db_session.create_session()
        return session.query(Users.Users).filter(Users.Users.login == self.login).one().password
        return cur.execute(SELECT password FROM Users
                               WHERE login = ?, (self.login,)).fetchone()[0]

'''

class LoginForm(FlaskForm):
    login = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Запомнить меня")
    submit_button = SubmitField("Войти")
    register_button = SubmitField("Зарегистрироваться")