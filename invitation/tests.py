from django.test import TestCase, Client
from django.contrib.auth.models import User as Invitation
from django.core.urlresolvers import reverse
from .models import Guest
from .forms import GuestForm
from unittest import skip


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

    @skip
    def test_invitation_form(self):
        form = InvitationForm({"name": "gupta"})
        self.assertTrue(form.is_valid)

    @skip
    def test_add_invitation_form_in_context(self):
        reponse = self.client.get(reverse("login"))
        self.assertContains(response.context["form"], InvitationForm)

    @skip
    def test_admin_logout(self):
        reponse = self.client.get(reverse("logout"))



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
        print(self.guest.username)
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
            self.guest.invitation = self.invitation
            self.guest.save()

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
            self.assertEqual(self.guest.invitation, self.invitation)

        def test_str_function(self):
            self.assertEqual(self.guest.__str__(), "Some Dummy")

        def test_guest_form(self):
            form = GuestForm({})
            self.assertTrue(form.is_bound)
            self.assertTrue(form.is_valid)
