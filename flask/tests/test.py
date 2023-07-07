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
from website.models import FuelOrderFormData
from website.models import ProfileData

testHash='sha256$tUTxRU3xmVxJzNWE$fee1d05e6f009bb4c4e3aaa5adaeb49ef2b37ce5f7090a62301c97b2fb0b1b21'

class WebsiteTests(TestCase):
    def create_app(self):
        website.DB_NAME = "testing.db"
        return create_app()

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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

    def test_home_when_profile_data_not_present(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.commit()
            self.client.post('login', data={'username': 'test', 'password': 'test'})
            response = self.client.get('/')
            self.assert_status(response, 200)
            self.assert_template_used('home.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', None)

    def test_home_when_profile_data_present(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.add(ProfileData(id=1))
            db.session.commit()
            self.client.post('login', data={'username': 'test', 'password': 'test'})
            response = self.client.get('/')
            self.assert_status(response, 200)
            self.assert_template_used('home.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', ProfileData.query.filter_by(id=1).first())

    def test_fuel_price_form_post(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.add(ProfileData(id=1))
            db.session.commit()
            self.client.post('login', data={'username': 'test', 'password': 'test'})
            response = self.client.get('/fuel_price_form')
            self.assert_status(response, 200)
            self.assert_template_used('fuel_price_form.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', ProfileData.query.filter_by(id=1).first())

    def test_sign_up_matching_passwords(self):
        with self.client:
            # Posting a request with matching passwords
            self.client.post('/sign-up', data={
            'username': 'test',
            'password': 'test',
            'confirm-password': 'test'
            })
            response = self.client.get('/sign-up')
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('sign_up.html')

            user = response.context['user']
            profile = response.context['profile']

            self.assertEqual(user, User.query.filter_by(id=1).first())
            self.assertEqual(profile, ProfileData.query.filter_by(id=1).first())

            # Posting a request with mismatching passwords
            self.client.post('/sign-up', data={
            'username': 'test2',
            'password': 'password1',
            'confirm-password': 'password2'
            })
            response = self.client.get('/sign-up')
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('sign_up.html')

    def test_sign_up_unique_usernames(self):
        with self.client:
        # Posting a request with a unique username
            self.client.post('/sign-up', data={
            'username': 'test',
            'password': 'test',
            'confirm-password': 'test'
            })
            response = self.client.get('/sign-up')
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('sign_up.html')

            user = response.context['user']
            profile = response.context['profile']

            self.assertEqual(user, User.query.filter_by(id=1).first())
            self.assertEqual(profile, ProfileData.query.filter_by(id=1).first())

            # Posting a request with an existing username
            existing_username = 'existing_user'
            existing_user = User(username=existing_username, password='password')
            db.session.add(existing_user)
            db.session.commit()

            self.client.post('/sign-up', data={
            'username': existing_username,
            'password': 'password123',
            'confirm-password': 'password123'
            })
            response = self.client.get('/sign-up')
            self.assertEqual(response.status_code, 200)
            self.assert_template_used('sign_up.html')

    def test_history(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.add(FuelOrderFormData(id=1,
                                             user_id = 1,
                                             gallons=1,
                                             delivery_date=datetime(2023, 1, 1),
                                             address_1='test',
                                             address_2='test',
                                             city='test',
                                             state='TX',
                                             zip_code='12345',
                                             in_state_status=True,
                                             price=1.0))
            db.session.add(ProfileData(id=1,
                                        full_name='test',
                                        address_1='test',
                                        address_2='test',
                                        city='test',
                                        state='TX',
                                        in_state_status=True,
                                        zip_code='12345',
                                        profile_completed=True))
            db.session.commit()

            loginResponse = self.client.post('/login', data={'username': 'test', 'password': 'test'})
            self.assert_status(loginResponse, 302)
            
            response = self.client.get('/view_history')

            self.assert200(response)
            self.assert_template_used('view_history.html')
            self.assert_context('orders', FuelOrderFormData.query.filter_by(user_id=1).all())
            self.assert_context('profile', ProfileData.query.filter_by(id=1).first())

if __name__ == '__main__':
    unittest.main()