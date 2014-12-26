import mock
import unittest
import transaction

from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    engine = create_engine('sqlite://')
    from fashion_designer.models import (
        Base,
        DBSession,
        Users,
        SignUpSheet,
        )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        user = Users(username='admin', password='password')
        signee = SignUpSheet(email='user@gmail.com')
        DBSession.add(user)
        DBSession.add(signee)
    return DBSession

class TestModels(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        self.session = _initTestingDB()

    def tearDown(self):
        testing.tearDown()
        self.session.remove()

    def test_user_in_database(self):
        from fashion_designer.models import Users
        username = 'admin'
        user_check = self.session.query(Users).filter_by(username=username).first()
        self.assertTrue(user_check)
        self.assertEqual(user_check.username, username)

    def test_user_notin_database(self):
        from fashion_designer.models import Users
        username = 'user'
        user_check = self.session.query(Users).filter_by(username=username).first()
        self.assertFalse(user_check)

    def test_user_already_signed_up(self):
        from fashion_designer.models import SignUpSheet
        email = 'user@gmail.com'
        check = SignUpSheet(email)
        self.assertTrue(check.is_duplicate_email())

    def test_new_user_not_signed_up(self):
        from fashion_designer.models import SignUpSheet
        email = 'newuser@gmail.com'
        check = SignUpSheet(email)
        self.assertFalse(check.is_duplicate_email())

    def test_password_is_hashed(self):
        from fashion_designer.models import Users
        username = 'user'
        password = 'password'
        add_user = Users(username, password)
        self.session.add(add_user)
        pwd_hash = add_user.check_pswd_hash(password)
        print pwd_hash



