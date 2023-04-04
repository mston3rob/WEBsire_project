import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    login = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_key_access = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    teacher = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
