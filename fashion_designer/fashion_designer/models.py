import bcrypt
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

    def is_duplicate_email(self):
        email_check = DBSession.query(SignUpSheet).filter_by(_email=self._email).first()
        if email_check:
            return True
        return False


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String (80))
    _password = Column('password', String(120), unique=True)
    _email = Column('email', String(80))
    is_activated = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value)

    def __init__(self, username, password):
        self.username = username
        self._password = password


    def username_exists(self):
        user = DBSession.query(Users).filter_by(username=self.username).first()
        if not user:
            return False
        return True

    def check_pswd_hash(self, password):
        hashed = DBSession.query(Users).filter_by(username=self.username).first()
        if bcrypt.hashpw(password, hashed._password) == hashed_password:
            return True
        else:
            return False

    def generate_password_hash(self, password):
        hashed = crypt.hashpw(password, bcrypt.gensalt(10))
        return hashed


Index('my_index', MyModel.name, unique=True, mysql_length=255)
