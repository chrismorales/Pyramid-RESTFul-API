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
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
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
    status = Column(Boolean, default=True)
    is_signed_up = Column(Boolean, default=True)
    date_signed_up = Column(DateTime, default=datetime.datetime.utcnow)
    _email = Column('email', String(80), nullable=False)

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
    status = Column(Boolean, default=True)
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
        self._password = self.generate_password_hash(value)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def username_exists(self):
        user = DBSession.query(Users).filter_by(username=self.username).first()
        if not user:
            return False
        return True

    def check_pswd_hash(self, password):
        hashed = DBSession.query(Users).filter_by(username=self.username).first()
        if bcrypt.hashpw(password, hashed._password) == hashed._password:
            return True
        else:
            return False

    def generate_password_hash(self, password):
        hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))
        return hashed

    def get_date_created(self):
        date = DBSession.query(Users).filter_by(username=self.username).first()
        return date.date_created


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    status = Column(Boolean, default=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    age = Column(Integer)
    sex = Column(String(20))
    location = Column(String(120))
    style = Column(String(120))
    friend_count = Column(Integer)


class Friend(Base):
    __tablename__ = 'friend'
    user_id = Column(Integer, ForeignKey(Users.user_id), primary_key=True)
    friend_id = Column(Integer, ForeignKey(Users.user_id), primary_key=True)
    request_status = Column(Boolean)
    user = relationship('Users', foreign_keys='Friend.user_id')
    friend = relationship('Users', foreign_keys='Friend.friend_id')


class Messages(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    created_by = Column(Integer, ForeignKey(Users.user_id), primary_key=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Boolean, default=True)
    msg = Column(String(120))


Index('my_index', MyModel.name, unique=True, mysql_length=255)
