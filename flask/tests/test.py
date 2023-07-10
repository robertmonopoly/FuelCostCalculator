import unittest
from flask_testing import TestCase
from datetime import datetime

import sys
sys.path.append('../')

# Used to modify db name
import website

from website import create_app
from website import db
from website.models import User
import glob

testHash='sha256$tUTxRU3xmVxJzNWE$fee1d05e6f009bb4c4e3aaa5adaeb49ef2b37ce5f7090a62301c97b2fb0b1b21'

class WebsiteTest(TestCase):
    def create_app(self):
        website.DB_NAME = "testing.db"
        return create_app()
    
    def login(self, username, password):
        response = self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
        self.assert200(response)
        self.assertTemplateUsed("home.html")
        self.assertContext('user', User.query.filter_by(username=username).first())

    def assertUserAnonymous(self):
        user = self.get_context_variable('user')
        self.assertEqual(user.is_anonymous, True)

    def login_and_create_user(self, username):
        db.session.add(User(username=username, password=testHash))
        db.session.commit()
        self.login(username, 'test')

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

def run_tests():
    test_files = glob.glob('*_tests.py')
    module_strings = [test_file[0:len(test_file)-3] for test_file in test_files]
    suites = [unittest.defaultTestLoader.loadTestsFromName(test_file) for test_file in module_strings]
    test_suite = unittest.TestSuite(suites)
    unittest.TextTestRunner().run(test_suite)

if __name__ == '__main__':
    run_tests()