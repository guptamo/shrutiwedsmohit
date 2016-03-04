from django.test import TestCase, Client
from django.core.urlresolvers import resolve, reverse
from django.contrib.auth.views import logout_then_login, logout
from . import views
from utils.testing import AdminTestBase


class SmokeTest(TestCase):

    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)


class HomePageTest(TestCase):

    def __init__(self, *args, **kwargs):
        super(HomePageTest, self).__init__(*args, **kwargs)
        self.base = AdminTestBase()

    def setUp(self):
        self.base.setUp()

    def tearDown(self):
        self.base.tearDown()

    def test_login_url_routing(self):
        # login url is at root hence "/"
        route = resolve(reverse("login"))
        self.assertEqual(route.func, views.login)

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
