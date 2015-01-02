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
    # status = Column(Boolean, default=True)
    is_signed_up = Column(Boolean, default=True)
    # date_signed_up = Column(DateTime, default=datetime.datetime.utcnow())
    _email = Column('email', String(80), nullable=False)

    def __init__(self, email):
        self._email = email

    def is_duplicate_email(self):
        email_check = DBSession.query(SignUpSheet).filter_by(
            _email=self._email).first()
        if email_check:
            return True
        return False

    def get_email(self):
        signup = DBSession.query(SignUpSheet).filter_by(_email=self._email).\
            first()
        return signup._email


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    # status = Column(Boolean, default=True)
    username = Column(String(80))
    _password = Column('password', String(120), unique=True)
    _email = Column('email', String(80))
    is_activated = Column(Boolean)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = self.generate_password_hash(value)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.set_status(email)

    def username_exists(self):
        user = DBSession.query(Users).filter_by(username=self.username).first()
        if not user:
            return False
        return True

    def check_pswd_hash(self, password):
        hashed = DBSession.query(Users).filter_by(
            username=self.username).first()
        if bcrypt.hashpw(password, hashed._password) == hashed._password:
            return True
        else:
            return False

    def generate_password_hash(self, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))
        return hashed

    def get_date_created(self):
        date = DBSession.query(Users).filter_by(username=self.username).first()
        return date.date_created

    def set_status(self, value):
        signup = SignUpSheet(value)
        if signup.get_email() == value:
            self.is_activated = True
        else:
            self.is_activated = False


class Profile(Base):
    __tablename__ = 'profile'
    user_id = Column(Integer, ForeignKey(Users.user_id), primary_key=True)
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


class SystemMessages(Base):
    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    page = Column(String(80))
    msg = Column(String(120))
    status = Column(Boolean, default=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    created_by = Column(Integer)

    def __init__(self, page, msg):
        self.page = page
        self.msg = msg


class Brands(Base):
    __tablename__ = 'brands'
    brand_id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    sizechart = relationship('SizingChart', uselist=False, backref="brands")

    def __init__(self, name):
        self.name = name


class SizingChart(Base):
    __tablename__ = 'sizechart'
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey(Brands.brand_id))
    clothes_type = Column(String(80), nullable=False)
    measurement = Column(Integer)
    size = Column(String(80), nullable=False)
    sex = Column(String(2), default='M')
    body_attr = relationship('ModelAttr', uselist=False, backref="sizechart")


class ModelAttr(Base):
    __tablename__ = 'bodyattributes'
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey(SizingChart.id))
    chest = Column(Integer)
    waist = Column(Integer)
    hip = Column(Integer)
    inner_leg = Column(Integer)

Index('my_index', MyModel.name, unique=True, mysql_length=255)
