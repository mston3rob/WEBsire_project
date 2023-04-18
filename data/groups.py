import sqlalchemy
from flask_login import UserMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import check_password_hash
from sqlalchemy_serializer import SerializerMixin


class Group(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    id_teacher = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=True)
    login_group = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    name_group = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    hashed_key_access = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=True)
    creator = sqlalchemy.Column(sqlalchemy.Boolean, index=True, nullable=True)