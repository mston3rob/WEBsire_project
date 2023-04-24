import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Test_tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'task_to_test'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_test = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    answers = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    true_answer = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
