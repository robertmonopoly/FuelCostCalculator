from flask_testing import TestCase
from test import WebsiteTest
from tests import testHash
from website import db
from website.models import User, ProfileData


class ProfileTests(WebsiteTest):
    def test_complete_profile_post(self):
        with self.client:
            db.session.add(User(id=1, username='test', password=testHash))
            db.session.commit()
            self.client.post('login', data={'username': 'test', 'password': 'test'}, follow_redirects=True)

            profileData = {
                'full_name': 'Test User',
                'address_1': '123 Test Street',
                'address_2': '',
                'city': 'Test City',
                'state': 'TX',
                'zip_code': '12345'
            }
            response = self.client.post('complete_profile', data=profileData, follow_redirects=True)
            self.assert_status(response, 200)

            user_profile = ProfileData.query.filter_by(id=1).first()
            self.assertIsNotNone(user_profile)

            # Convert the user_profile SQLAlchemy object into a dictionary
            user_profile_dict = {
                'full_name': user_profile.full_name,
                'address_1': user_profile.address_1,
                'address_2': user_profile.address_2,
                'city': user_profile.city,
                'state': user_profile.state,
                'zip_code': user_profile.zip_code
            }

            self.assertEqual(user_profile_dict, profileData)
