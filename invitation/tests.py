from django.test import TestCase, Client
from django.contrib.auth.models import User as Invitation
from django.core.urlresolvers import reverse
from .models import Guest


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

    def test_guest_cannot_access_dashboard(self):
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertRedirects(
            response,
            expected_url=reverse("invitation:invitation"))


class GuestModelTests(TestCase):

        def setUp(self):
            self.boolean_fields = [
                "invited_sangeet",
                "invited_reception",
                "invited_ceremony",
                "attending_sangeet",
                "attending_reception",
                "attending_ceremony"]

            self.guest = Guest.objects.create(
                name="Some Dummy",
                invited_by="gupta")
            self.invitation = Invitation.objects.create()

        def tearDown(self):
            self.guest.delete()

        def test_guest_model_save(self):
            self.assertEqual(Guest.objects.count(), 1)

        def test_guest_model_save_defaults(self):
            self.assertEqual(self.guest.name, "Some Dummy")
            self.assertEqual(self.guest.invited_by, "gupta")
            for field in self.boolean_fields:
                self.assertFalse(getattr(self.guest, field))
            self.assertEqual(self.guest.meal_choice, "")
            self.assertEqual(self.guest.note, "")

        def test_unicode_function(self):
            self.assertEqual(self.guest.__unicode__(), "Some Dummy")
