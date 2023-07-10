from test import WebsiteTest
from flask_login.mixins import AnonymousUserMixin

from website import db
from website.models import User

class SignupTests(WebsiteTest):
    def test_sign_up_matching_passwords(self):
        with self.client:
            response = self.client.post('/sign-up', data={
                'username': 'test',
                'password': 'test',
                'confirm-password': 'test'
            }, follow_redirects=True)

            self.assert200(response)
            self.assertTemplateUsed('home.html')
            self.assertContext('user', User.query.filter_by(id=1).first())

    def test_sign_up_returns_page(self):
        with self.client:
            response = self.client.get('/sign-up')
            self.assert200(response)
            self.assertTemplateUsed('sign_up.html')
            self.assertUserAnonymous()

    def test_sign_up_mismatching_passwords(self):
        with self.client:
            response = self.client.post('/sign-up', data={
                'username': 'test2',
                'password': 'password1',
                'confirm-password': 'password2'
            })
            self.assert200(response)
            self.assertTemplateUsed('sign_up.html')
            self.assertMessageFlashed('The supplied passwords do not match', category='error')
            self.assertUserAnonymous()

    def test_sign_up_existing_usernames(self):
        with self.client:
            db.session.add(User(username='test', password='password'))
            db.session.commit()

            response = self.client.post('/sign-up', data={
                'username': 'test',
                'password': 'password123',
                'confirm-password': 'password123'
            })

            self.assert200(response)
            self.assertMessageFlashed('A user already exists with that username', category='error')
            self.assertUserAnonymous()