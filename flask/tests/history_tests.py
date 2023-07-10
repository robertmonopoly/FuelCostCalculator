from test import WebsiteTest, testHash
from datetime import datetime
from website import db
from website.models import User, FuelOrderFormData, ProfileData

class HistoryTests(WebsiteTest):
    def test_history(self):
        with self.client:
            self.login_and_create_user('test')
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
            
            response = self.client.get('/view_history')

            self.assert200(response)
            self.assert_template_used('view_history.html')
            self.assert_context('orders', FuelOrderFormData.query.filter_by(user_id=1).all())
            self.assert_context('profile', ProfileData.query.filter_by(id=1).first())