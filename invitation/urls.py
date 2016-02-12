from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^invitation/$', views.invitation, name="invitation")
]
