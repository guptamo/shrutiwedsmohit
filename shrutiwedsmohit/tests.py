from django.test import TestCase, Client
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.views import logout_then_login, logout, login
from . import views
from utils.testing import AdminTestBase, GuestTestBase
from invitation.models import Invitation


class SmokeTest(TestCase):

    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)


class GuestPageTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(GuestPageTest, self).__init__(*args, **kwargs)
        self.base = GuestTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client
        self.invitation = lambda: Invitation.objects.create(
            name=self.base.guest.username,
            user=self.base.guest
        )

    def tearDown(self):
        self.base.tearDown()

    def test_redirect_to_login_redirect_on_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "guest", "password": "guest"},
            follow=True)
        self.assertIn(
            (reverse("login_redirect"), 302),
            response.redirect_chain)

    def test_redirect_to_invitation_on_login_for_guests(self):
        invitation = self.invitation()
        response = self.client.get(reverse("login_redirect"))
        self.assertRedirects(
            response,
            reverse("invitation:invitation", args=[self.base.guest.username])
        )


class HomePageTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(HomePageTest, self).__init__(*args, **kwargs)
        self.base = AdminTestBase()

    def setUp(self):
        self.base.setUp()
        self.client = self.base.client

    def tearDown(self):
        self.base.tearDown()

    def test_login_url_routing(self):
        # login url is at root hence "/"
        route = resolve(reverse("login"))
        self.assertEqual(route.func, login)

    def test_logout_url_routing(self):
        route = resolve(reverse("logout"))
        self.assertEqual(route.func, logout_then_login)

    def test_logout_redirect_to_login(self):
        response = self.client.get(reverse("logout"))
        self.assertRedirects(response, reverse("login"))

    def test_login_template_loading(self):
        response = self.client.get(reverse("login"))
        self.assertIn(b'<title>Login', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))

    def test_login_redirects_admins_to_dashboard(self):
        response = self.client.get(reverse("login_redirect"))
        self.assertRedirects(
            response,
            reverse("invitation:dashboard")
        )
