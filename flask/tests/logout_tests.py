from test import WebsiteTest, testHash

from website import db
from website.models import User

class LogoutTests(WebsiteTest):
    def test_logout(self):
        with self.client:
            self.login_and_create_user('test')

            response = self.client.get('/logout', follow_redirects=True)
            
            self.assert200(response)
            self.assertTemplateUsed("login.html")
            self.assertUserAnonymous()