from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import login as actual_login
from invitation.views import login_redirect
from django.shortcuts import render


def login(request):
    if request.user.is_anonymous():
        return actual_login(
            request,
            template_name="invitation/login.html",
            extra_context={"next": reverse_lazy("invitation:login_redirect")})
    else:
        return login_redirect(request)
