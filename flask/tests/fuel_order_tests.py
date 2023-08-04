from test import WebsiteTest, testHash

from website import db
from website.models import User, ProfileData, FuelOrderFormData

class FuelOrderTest(WebsiteTest):
    def test_fuel_price_form_data_present(self):
        with self.client:
            self.login_and_create_user('test')
            profile = ProfileData(id=1)
            fuel_order_form_data = FuelOrderFormData(id=1, gallons=100, address_1='123 Street')
            db.session.add_all([profile, fuel_order_form_data])
            db.session.commit()
            
            response = self.client.get('/fuel_price_form')
            
            self.assert200(response)
            self.assert_template_used('fuel_price_form.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', profile)

    def test_fuel_price_form_data_not_present(self):
        with self.client:
            self.login_and_create_user('test')
            
            response = self.client.get('/fuel_price_form')

            self.assert_status(response, 200)
            self.assert_template_used('fuel_price_form.html')
            self.assert_context('user', User.query.filter_by(id=1).first())
            self.assert_context('profile', None)

    def test_fuel_price_form_out_of_state_new_customer(self):
        with self.client:
            self.login_and_create_user('test')
            profile = ProfileData(id=1, profile_completed=True)
            fuel_order_form_data = FuelOrderFormData(id=1, gallons=1500, address_1='123 Street')
            db.session.add_all([profile, fuel_order_form_data])
            db.session.commit()
            
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
                'delivery_date': '2023-12-09',  # Set the delivery date
                'form_type': 'fuel_order'
            })

            self.assert_context('address_1', ProfileData.query.filter_by(id=1).first().address_1)
            self.assert_context('price_per_gallon', expected_price_per_gallon)
            self.assert_context('price', expected_price)