import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class GroupTest(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups_tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_teacher = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # id учителя что выложил
    id_group = sqlalchemy.Column(sqlalchemy.String, nullable=True)  # id группы для выкладывания
    id_questions = sqlalchemy.Column(sqlalchemy.String, nullable=True) # id вопросов (через ;)
    block_list = sqlalchemy.Column(sqlalchemy.String, nullable=True) # если тест не для всех учеников группы (исключение)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True) # количество прохождений
    time = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True) # время для прохождения
