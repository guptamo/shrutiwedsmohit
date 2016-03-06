from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'dashboard/$', views.dashboard, name="dashboard"),
    url(r'add-invitation/$', views.add_invitation, name="add_invitation"),
    url(r'(?P<invitation_name>[\w]+)/$', views.invitation, name="invitation"),
]
