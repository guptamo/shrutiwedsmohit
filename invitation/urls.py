from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'(?P<invitation_name>[\w]+)/$', views.invitation, name="invitation"),
    url(r'add-invitation/$', views.add_invitation, name="add_invitation"),
    url(r'dashboard/$', views.dashboard, name="dashboard"),
]
