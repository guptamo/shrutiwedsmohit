from .base import BaseTest
from django.contrib.auth.models import User as Invitation


class AdministratorTest(BaseTest):

    def setUp(self):
        super().setUp()

        self.admin = Invitation.objects.create_superuser(
            username="admin",
            email="admin@hotmail.com",
            password="admin")

    def test_admin_login(self):
        # Surprise surprise! We have more guests coming! Mohit would like to
        # create a new invitation to allow his *ahem* beloved guest could log
        # in to the beautiful website.

        self.browser.get(self.server_url)
        self.assertIn('Login', self.browser.title)

        # Mohit confirms he's on the right page and is delighted to see Login,
        # in big bold letters. He enters his admin username and password and
        # clicks login to be brought to the add invitation page.

        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('admin')
        self.browser.find_element_by_id('login').click()

