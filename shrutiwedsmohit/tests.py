from django.test import TestCase, Client
from django.core.urlresolvers import resolve
from django.contrib.auth.views import login


class SmokeTest(TestCase):

    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)


class HomePageTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_login_url_routing(self):
        # login url is at root hence "/"
        route = resolve("/")
        self.assertEqual(route.func, login)

    def test_login_template_loading(self):
        response = self.client.get("/")
        self.assertIn(b'<title>Login', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
