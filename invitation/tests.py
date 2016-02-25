from django.test import TestCase, Client
from django.contrib.auth.models import User as Invitation
from django.core.urlresolvers import reverse


class AdminFunctionsTests(TestCase):

    def setUp(self):
        self.admin = Invitation.objects.create_superuser(
            username="admin",
            email="admin@hotmail.com",
            password="admin")
        self.client = Client()
        self.client.login(
            username="admin",
            password="admin")

    def tearDown(self):
        self.admin.delete()

    def test_admin_login_redirect(self):
        response = self.client.get(reverse("login"))
        self.assertRedirects(
            response,
            expected_url=reverse("invitation:dashboard"))


class GuestFunctionsTests(TestCase):

    def setUp(self):
        self.guest = Invitation.objects.create_user(
            username="guest",
            email="guest@hotmail.com",
            password="guest")
        self.client = Client()
        self.client.login(
            username="guest",
            password="guest")

    def tearDown(self):
        self.guest.delete()

    def test_guest_login_redirect(self):
        response = self.client.get(reverse("login"))
        self.assertRedirects(
            response,
            expected_url=reverse("invitation:invitation"))
