import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups_tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_questions = sqlalchemy.Column(sqlalchemy.String, nullable=True) # id вопросов
    login = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # login группы для выкладывания
    block_list = sqlalchemy.Column(sqlalchemy.String, nullable=True) # если тест не для всех учеников группы (исключение)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # количество прохождений
    time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True) # время для прохождения

