from django.test import TestCase, Client
from django.core.urlresolvers import resolve, reverse
from . import views


class SmokeTest(TestCase):

    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)


class HomePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_url_routing(self):
        # login url is at root hence "/"
        route = resolve(reverse("login"))
        self.assertEqual(route.func, views.login)

    def test_login_template_loading(self):
        response = self.client.get(reverse("login"))
        self.assertIn(b'<title>Login', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
