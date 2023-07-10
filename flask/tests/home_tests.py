from test import WebsiteTest, testHash

from website import db
from website.models import User, ProfileData

class HomeTests(WebsiteTest):
    def test_home_when_profile_complete(self):
        with self.client:
            self.login_and_create_user('test')
            db.session.add(ProfileData(id=1))
            db.session.commit()

            response = self.client.get('/')

            self.assert200(response)
            self.assertTemplateUsed('home.html')
            self.assertContext('user', User.query.filter_by(id=1).first())
            self.assertContext('profile', ProfileData.query.filter_by(id=1).first())

    def test_home_profile_incomplete(self):
        with self.client:
            self.login_and_create_user('test')
            response = self.client.get('/')

            self.assertStatus(response, 200)
            self.assertTemplateUsed('home.html')
            self.assertContext('user', User.query.filter_by(id=1).first())
            self.assertContext('profile', None)