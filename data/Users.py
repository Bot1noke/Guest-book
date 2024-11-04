import sqlalchemy as sa
import sqlalchemy.orm as orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'Users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, nullable=False)
    login = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)

    def check_user(self, password):
        return check_password_hash(self.password, password)
    #comments = orm.relation("Comments", back_populates='users', cascade='all, delete')
    #articles = orm.relation("Articles", back_populates='users', cascade='all, delete')

