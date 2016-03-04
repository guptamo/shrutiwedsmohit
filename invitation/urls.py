from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add-invitation/$', views.add_invitation, name="add_invitation"),
    url(r'dashboard/$', views.dashboard, name="dashboard"),
]
