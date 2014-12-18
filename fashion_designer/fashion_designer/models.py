import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    value = Column(Integer)


class SignUpSheet(Base):
    __tablename__ = 'signup'
    id = Column(Integer, primary_key=True)
    _email = Column('email', String(80), nullable=False)
    is_signed_up = Column(Boolean, default=True)

    def __init__(self, email):
        self._email = email


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String (80))
    _password = Column('password', String(120), unique=True)
    _email = Column('email', String(80), nullable=False)
    is_activated = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, username, password, email):
        self.username = username
        self._password = password
        self._email = email

Index('my_index', MyModel.name, unique=True, mysql_length=255)
