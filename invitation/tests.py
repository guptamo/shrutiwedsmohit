from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .models import Guest, Invitation
from .forms import GuestForm, InvitationForm
from .views import password_generator
from unittest import skip


class AdminBaseTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@hotmail.com",
            password="admin")
        self.client = Client()
        self.client.login(
            username="admin",
            password="admin")

    def tearDown(self):
        self.admin.delete()


class GuestBaseTest(TestCase):

    def setUp(self):
        self.guest = User.objects.create_user(
            username="guest",
            email="guest@hotmail.com",
            password="guest")
        self.client = Client()
        self.client.login(
            username="guest",
            password="guest")

    def tearDown(self):
        self.guest.delete()


class AdminFunctionsTests(AdminBaseTest):
    pass


class GuestFunctionsTests(GuestBaseTest):
    pass


class GuestModelTests(TestCase):

    def setUp(self):
        self.boolean_fields = [
            "attending_sangeet",
            "attending_reception",
            "attending_ceremony"]

        self.guest = Guest.objects.create(name="Some Dummy")
        self.invitation = Invitation.objects.create()
        self.guest.invitation = self.invitation
        self.guest.save()

    def tearDown(self):
        self.guest.delete()

    def test_guest_model_save(self):
        self.assertEqual(Guest.objects.count(), 1)

    def test_guest_model_save_defaults(self):
        self.assertEqual(self.guest.name, "Some Dummy")
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


class InvitationModelTests(AdminBaseTest):

    def test_add_invitation_form_in_dashboard_context(self):
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertIsInstance(response.context['form'], InvitationForm)

    def test_posting_to_add_invitation_view(self):
        data = {
            "name": "schmoe",
            "invited_by": "gupta",
            "invited_sangeet": False,
            "invited_ceremony": False,
            "invited_reception": False,}

        response = self.client.post(reverse("invitation:add_invitation"), data)
        self.assertRedirects(response, reverse("invitation:dashboard"))

    def test_password_generator(self):
        self.assertEqual(password_generator("michael1"), "704111")

    def test_add_invitation_view_creates_invitation_objects(self):
        data = {
            "name": "michael",
            "invited_by": "gupta",
            "invited_sangeet": False,
            "invited_ceremony": False,
            "invited_reception": False,}

        response = self.client.post(reverse("invitation:add_invitation"), data)
        self.assertEqual(Invitation.objects.count(), 1)
        self.assertEqual(User.objects.count(), 2)
