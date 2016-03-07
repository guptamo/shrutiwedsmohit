from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from .models import Guest, Invitation
from .forms import GuestForm, InvitationForm, AddGuestForm
from .views import password_generator, dashboard
from unittest import skip
from utils.testing import AdminTestBase, GuestTestBase


class AdminFunctionsTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(AdminFunctionsTests, self).__init__(*args, **kwargs)
        self.base = AdminTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client

    def tearDown(self):
        self.base.tearDown()

    def test_invitation_lists_in_dashboard_context(self):
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertTrue(all(
            isinstance(invitation, Invitation)
                for invitation in response.context["invitations"]))
        self.assertIsNotNone(response.context["invitations"])

    def test_invitations_display_on_dashboard(self):
        invitation = Invitation.objects.create()
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertInHTML("<h2>Invitations</h2>", response.content.decode())

    def test_invitations_do_not_display_if_no_invitations(self):
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertInHTML(
            "<h2>You Haven't Invited Anyone Yet...Do It!</h2>",
            response.content.decode())


class GuestFunctionsTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(GuestFunctionsTests, self).__init__(*args, **kwargs)
        self.base = GuestTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client

    def tearDown(self):
        self.base.tearDown()

    def test_guest_form_in_context(self):
        response = self.client.get(
            reverse("invitation:invitation", args=[self.base.guest.username]))
        self.assertIsInstance(response.context["form"], GuestForm)


class GuestModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(GuestModelTests, self).__init__(*args, **kwargs)
        self.base = GuestTestBase()

    def setUp(self):
        self.base.setUp()
        self.boolean_fields = [
            "attending_sangeet",
            "attending_reception",
            "attending_ceremony"]
        self.invitation = Invitation.objects.create(user=self.base.guest)
        self.guest = Guest.objects.create(
            invitation=self.invitation,
            name="Some Dummy")

    def tearDown(self):
        self.base.tearDown()

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

    def test_add_guest_form(self):
        form = AddGuestForm({"name": self.base.guest.username})
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid)


class InvitationModelTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(InvitationModelTests, self).__init__(*args, **kwargs)
        self.base = AdminTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client

    def tearDown(self):
        self.base.tearDown()

    def test_add_invitation_form_in_dashboard_context(self):
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertIsInstance(response.context['form'], InvitationForm)

    def test_posting_to_add_invitation_view_redirects_to_dashboard(self):
        data = {
            "name": "schmoe",
            "invited_by": "gupta",
            "invited_sangeet": False,
            "invited_ceremony": False,
            "invited_reception": False,}

        response = self.client.post(reverse("invitation:add_invitation"), data)
        self.assertRedirects(response, reverse("invitation:dashboard"))

    def test_password_generator(self):
        self.assertEqual(password_generator("Michael1"), "704111")

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
