from . import base
from django.contrib.auth.models import User as Invitation


class AdministratorTests(base.BaseTest):

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
        self.assertIn(
            "Login | Shruti and Mohit's Wedding Site",
            self.browser.title)

        # Mohit confirms he's on the right page and is delighted to see Login,
        # in big bold letters. He enters his admin username and password and
        # clicks login to be brought to the add invitation page.

        self.browser.find_element_by_id('id_username').send_keys('admin')
        self.browser.find_element_by_id('id_password').send_keys('admin')
        self.browser.find_element_by_id('login').click()

        # Mohit is happy to see that his Django app hasn't broken yet. The
        # page title says add invitation and he's exactly where he needs to
        # be.
        self.assertIn("Dashboard", self.browser.title)


class GuestTests(base.BaseTest):

    def setUp(self):
        super().setUp()

        self.guest = Invitation.objects.create_user(
            username="guest",
            email="guest@hotmail.com",
            password="guest")

    def test_guest_login(self):
        # Sonnika would like to RSVP to Shruti and Mohit's wedding, as well as
        # check out some of the pictures. She gets out her wedding invitation
        # and types in the url on the invite.

        self.browser.get(self.server_url)
        self.assertIn(
            "Login | Shruti and Mohit's Wedding Site",
            self.browser.title)

        # Sonnika has been working on her typing skills and gets the url right
        # on the first try without crying. She enters all the login information
        # that is on the invite and crosses her fingers.

        self.browser.find_element_by_id('id_username').send_keys('guest')
        self.browser.find_element_by_id('id_password').send_keys('guest')
        self.browser.find_element_by_id('login').click()

        # Success! She's a winner and sees that she actually is invited. She is
        # greeted by navigation, a big beautiful cover picture, and a few forms
        # for her to rsvp in.

        self.assertIn("Celebrate with us!", self.browser.title)
