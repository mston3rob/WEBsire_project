import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True) # вопрос
    variant_answers = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True) # все варианты ответа
    correct_answer = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True) # правильный ответ(ы)
    points = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # баллы за ответ
    img = sqlalchemy.Column(sqlalchemy.BLOB, index=True, nullable=True) # изобрадение к тесту
