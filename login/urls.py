from django.conf.urls import url
from django.contrib.auth.views import login
from . import views

urlpatterns = [
    url(r'admin-redirect/$', views.admin_redirect, name="admin_redirect"),
    url(r'add-invitation/$', views.add_invitation, name="add_invitation"),
    url(r'^$', login,
        {"template_name": "login/login.html",
            "next": "/admin-redirect/", },
        name="login"),
]
