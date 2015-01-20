"""
                        *functional_test.py*

        This module handles testing all the major functions
        of the application such as login, signup, sending mail,
        ... etc.
"""
import unittest
import transaction

from pyramid import testing

class FunctionalTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_login_view(self):
        """ Checks the login view works """
        # Use a dummy request and make sure the url exists
        pass
