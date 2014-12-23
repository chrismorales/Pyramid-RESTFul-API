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
        )
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        user = Users(username='admin', password='password')
        DBSession.add(user)
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
