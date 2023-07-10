from test import WebsiteTest, testHash

from website import db
from website.models import User

class LoginTests(WebsiteTest):
    def test_login_when_user_doesnt_exist(self):
        with self.client:
            loginResponse = self.client.post('login', data={'username': 'test', 'password': 'test'})
            self.assert200(loginResponse)
            self.assert_message_flashed('Invalid credentials', category='error')
            self.assert_template_used('login.html')

    def test_login_when_credentials_invalid(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.commit()
            loginResponse = self.client.post('login', data={'username': 'test', 'password': 'test2'})
            self.assert200(loginResponse)
            self.assert_message_flashed('Invalid credentials, try again.', category='error')
            self.assert_template_used('login.html')

    def test_login_when_credentials_valid(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.commit()
            loginResponse = self.client.post('login', data={'username': 'test', 'password': 'test'}, follow_redirects=True)
            self.assert_status(loginResponse, 200)
            self.assert_template_used('home.html')
            self.assert_context('user', User.query.filter_by(id=1).first())