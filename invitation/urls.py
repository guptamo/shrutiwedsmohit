from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'dashboard/$', views.dashboard, name="dashboard"),
    url(r'add-invitation/$', views.add_invitation, name="add_invitation"),
    url(
        r'(?P<invitation_name>[\w-]+)/add-guest/$',
        views.add_guest,
        name="add_guest"
    ),
    url(r'(?P<invitation_name>[\w-]+)/(?P<guest_pk>[\d]+)/$',
        views.update_guest,
        name="update_guest"
    ),
    url(r'(?P<invitation_name>[\w-]+)/$', views.invitation, name="invitation"),
]
