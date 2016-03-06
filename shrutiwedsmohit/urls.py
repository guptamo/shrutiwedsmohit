from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login, login
from django.core.urlresolvers import reverse_lazy
from .views import login_redirect

urlpatterns = [
    url(r'^logout/$', logout_then_login, name="logout"),
    url(r'^invitation/', include("invitation.urls", namespace="invitation")),
    url(r'^admin/', admin.site.urls),
    url(r'^login-redirect/$', login_redirect, name="login_redirect"),
    url(r'^$',
        login,
        {"template_name": "invitation/login.html"},
        name="login"),
]
