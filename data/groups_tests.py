import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups_tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_questions = sqlalchemy.Column(sqlalchemy.String, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True, autoincrement=True)
    # time
    attemps = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
