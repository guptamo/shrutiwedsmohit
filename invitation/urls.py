from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.invitation, name="invitation"),
    url(r'admin-redirect/$', views.admin_redirect, name="admin_redirect"),
    url(r'add-invitation/$', views.add_invitation, name="add_invitation"),
]
