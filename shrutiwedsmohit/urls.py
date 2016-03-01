from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from . import views


urlpatterns = [
    url(r'^$', views.login, name="login"),
    url(r'^logout/$', logout_then_login, name="logout"),
    url(r'^invitation/', include("invitation.urls", namespace="invitation")),
    url(r'^admin/', admin.site.urls),
]
