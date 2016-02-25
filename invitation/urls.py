from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.invitation, name="invitation"),
    url(r'login-redirect/$', views.login_redirect, name="login_redirect"),
    url(r'dashboard/$', views.dashboard, name="dashboard"),
]
