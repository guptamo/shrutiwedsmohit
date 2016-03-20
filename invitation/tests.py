from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, resolve
from .models import Guest, Invitation
from .forms import InvitationForm, AddGuestForm, UpdateGuestForm
from .views import dashboard, update_guest
from unittest import skip
from utils.testing import AdminTestBase, GuestTestBase


class AdminFunctionsTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(AdminFunctionsTests, self).__init__(*args, **kwargs)
        self.base = AdminTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client
        self.invitation = lambda: Invitation.objects.create(name="testinvite")

    def tearDown(self):
        self.base.tearDown()

    @skip
    def test_invitation_lists_in_dashboard_context(self):
        response = self.client.get(reverse("invitation:dashboard"))
        self.assertTrue(all(
            isinstance(invitation, (Invitation, str))
                for invitation in response.context["invite_info"]))
        self.assertIsNotNone(response.context["invite_info"])

    def test_posting_add_guest_form_to_add_guest_view_creates_guest(self):
        invitation = self.invitation()
        response = self.client.post(
            reverse("invitation:add_guest", args=[invitation.name]),
            {"name": "Test Guest"}
        )
        invitation.refresh_from_db()
        guest = invitation.guest_set.all()
        self.assertEqual(guest[0].name, "Test Guest")

    def test_posting_add_guest_form_to_add_guest_view_redirects_to_invitation(self):
        invitation = self.invitation()
        response = self.client.post(
            reverse("invitation:add_guest", args=[invitation.name]),
            {"name": "Test Guest"}
        )
        self.assertRedirects(response, invitation.get_absolute_url())

    def test_add_guest_form_in_invitation_context(self):
        invitation = self.invitation()
        response = self.client.get(invitation.get_absolute_url())
        self.assertIsInstance(response.context["add_guest_form"], AddGuestForm)

    def test_guest_formset_invitation_context(self):
        invitation = self.invitation()
        response = self.client.get(invitation.get_absolute_url())
        self.assertTrue(
            all(
                isinstance(guest, (Guest, UpdateGuestForm)) for guest in response.context["guest_list"]
            )
        )

class GuestFunctionsTests(TestCase):

    def __init__(self, *args, **kwargs):
        super(GuestFunctionsTests, self).__init__(*args, **kwargs)
        self.base = GuestTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client
        self.invitation = Invitation.objects.create(name="testinvite")
        self.invitation.user = self.base.guest
        self.invitation.save()
        self.factory = RequestFactory()

    def tearDown(self):
        self.base.tearDown()
        self.invitation.delete()

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
        self.invitation = Invitation.objects.create(
            user=self.base.guest,
            name="testinvite"
        )
        self.guest = lambda: Guest.objects.create(
            invitation=self.invitation,
            name="Some Dummy"
        )

    def tearDown(self):
        self.base.tearDown()

    def test_guest_model_save(self):
        guest = self.guest()
        self.assertEqual(Guest.objects.count(), 1)

    def test_guest_model_save_defaults(self):
        guest = self.guest()
        self.assertEqual(guest.name, "Some Dummy")
        for field in self.boolean_fields:
            self.assertFalse(getattr(guest, field))
        self.assertEqual(guest.meal_choice, "")
        self.assertEqual(guest.note, "")
        self.assertEqual(guest.invitation, self.invitation)

    def test_str_function(self):
        guest = self.guest()
        self.assertEqual(guest.__str__(), "Some Dummy")

    def test_add_guest_form(self):
        form = AddGuestForm({"name": self.base.guest.username})
        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid)

    @skip
    def test_guest_add_form_view_saves_new_guests(self):
        response = self.client.post(
            reverse("invitation:add_guest", args=[self.invitation.name]),
            {"name": "Some Guy"}
        )
        self.invitation.refresh_from_db()
        guests = self.invitation.guest_set.all()
        # guests = Guest.objects.filter(invitation__name=self.invitation.name)
        print(guests)
        self.assertEqual(guests[0].name, "Some Guy")

    def test_update_guests_url_resolves_properly(self):
        guest = self.guest()
        route = resolve(reverse(
            "invitation:update_guest",
            args=[self.invitation.name, guest.pk]
        ))
        self.assertEqual(route.func, update_guest)

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
        invitation = Invitation.objects.create(name="Michael1")
        self.assertEqual(invitation.password(), "704111")

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

    def test_invitation_get_absolute_url(self):
        invitation = Invitation.objects.create(name="testinvite")
        self.assertEqual(
            invitation.get_absolute_url(),
            reverse("invitation:invitation", args=[invitation.name])
        )
