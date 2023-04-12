import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_teacher = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # кто выложил тест
    id_group = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # для кого выложен
    question = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True) # вопрос
    correct_answer = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True) # правильный ответ
    points = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # баллы за ответ
    variant = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # вариант