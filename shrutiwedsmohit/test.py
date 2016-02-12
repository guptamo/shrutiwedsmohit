from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.contrib.auth.views import login


class SmokeTest(TestCase):

    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)


class HomePageTest(TestCase):

    def test_login_url_routing(self):
        # login url is at root hence "/"
        route = resolve("/")
        self.assertEqual(route.func, login)

    def test_login_template_loading(self):
        request = HttpRequest()
        response = login(request)
        self.assertIn(b'<title> Login', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
