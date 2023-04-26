import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Test_tasks(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'task_to_test'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_test = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tests.id"))
    num_in_test = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    question = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    answers = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    true_answer = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    type_answer = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    cost = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    img = sqlalchemy.Column(sqlalchemy.BLOB, nullable=True)
    test = orm.relationship('Tests')