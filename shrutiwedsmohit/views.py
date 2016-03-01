from django.core.urlresolvers import reverse
from django.contrib.auth.views import login as actual_login
from django.shortcuts import render


def login(request):
    return actual_login(
        request,
        template_name="invitation/login.html",
        extra_context={"next": reverse("invitation:dashboard")})
