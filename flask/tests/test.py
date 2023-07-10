import unittest
from flask_testing import TestCase
from datetime import datetime
import math

import sys
sys.path.append('../')

# Used to modify db name
import website

from website import create_app
from website import db
from werkzeug.security import generate_password_hash
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

    def test_fuel_price_form_data_present(self):
        with self.client:
            user = User(id=1, username='test', password=testHash)
            profile = ProfileData(id=1)
            fuel_order_form_data = FuelOrderFormData(id=1, gallons=100, address_1='123 Street')
            db.session.add_all([user, profile, fuel_order_form_data])
            db.session.commit()
            
            self.client.post('/login', data={'username': 'test', 'password': 'test'})
            
            response = self.client.get('/fuel_price_form')
            self.assert200(response)
            self.assert_template_used('fuel_price_form.html')
            self.assert_context('user', user)
            self.assert_context('profile', profile)

    def test_fuel_price_form_data_not_present(self):
        with self.client:
            db.session.add(User(id = 1, username='test', password=testHash))
            db.session.commit()
            self.client.post('login', data={'username': 'test', 'password': 'test'})
            response = self.client.get('/fuel_price_form')
            self.assert_status(response, 200)
            self.assert_template_used('fuel_price_form.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', None)

    def test_fuel_price_form_out_of_state_new_customer(self):
        with self.client:
            user = User(id=1, username='test', password=testHash)
            profile = ProfileData(id=1, profile_completed=True)
            fuel_order_form_data = FuelOrderFormData(id=1, gallons=1500, address_1='123 Street')
            db.session.add_all([user, profile, fuel_order_form_data])
            db.session.commit()
            self.client.post('login', data={'username': 'test', 'password': 'test'})
            response = self.client.get('/fuel_price_form')
            self.assert_status(response, 200)
            self.assert_template_used('fuel_price_form.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', ProfileData.query.filter_by(id=1).first())

            gallons = 1500
            current_price = 1.50
            location_factor = 0.04  # Assuming out of Texas
            history_factor = 0 # Updated assumption for new customer
            requested_factor = 0.02  # Assuming more than 1000 gallons
            profit_factor = 0.1

            company_profit_margin = current_price * (location_factor - history_factor + requested_factor + profit_factor)

            expected_price_per_gallon = current_price + company_profit_margin
            expected_price = gallons * expected_price_per_gallon

            # POST request to the '/fuel_price_form' route
            response = self.client.post('/fuel_price_form', data={
                'gallons_requested': '1500',  # Set the desired gallons
                'delivery_date': '2023-12-09'  # Set the delivery date
            })

            self.assert_context('address_1', ProfileData.query.filter_by(id=1).first().address_1)
            self.assert_context('price_per_gallon', expected_price_per_gallon)
            self.assert_context('price', expected_price)

    def test_sign_up_invalid_username(self):
        response = self.client.post('/sign-up', data={
            'username': 'invalid-username!',
            'password': 'test',
            'confirm-password': 'test'
        }, follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('sign_up.html')
        self.assertIn(b'Invalid username format', response.data)
        self.assertIsNone(User.query.filter_by(username='invalid-username!').first())

    def test_sign_up_password_mismatch(self):
        response = self.client.post('/sign-up', data={
            'username': 'test',
            'password': 'password1',
            'confirm-password': 'password2'
        }, follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('sign_up.html')
        self.assertIn(b'The supplied passwords do not match', response.data)
        self.assertIsNone(User.query.filter_by(username='test').first())
        # Additional assertions or checks as needed

    def test_sign_up_existing_username(self):
        db.session.add(User(username='test', password=generate_password_hash('test')))
        db.session.commit()
        response = self.client.post('/sign-up', data={
            'username': 'test',
            'password': 'test',
            'confirm-password': 'test'
        }, follow_redirects=True)
        self.assert200(response)
        self.assert_template_used('sign_up.html')
        self.assertIn(b'A user already exists with that username', response.data)
        # Additional assertions or checks as needed    

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
