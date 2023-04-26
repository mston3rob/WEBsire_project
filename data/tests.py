import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Tests(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_teacher = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # кто выложил тест
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    questions = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True) # вопрос
    test_redacting = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    time_test = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    to_who = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_published = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    tasks = orm.relationship("Test_tasks", back_populates='test')