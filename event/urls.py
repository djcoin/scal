
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.EventList.as_view(), name="event_list"),
    url(r'^create$', views.EventCreate.as_view(), name="event_create"),
    url(r'^edit/(?P<pk>\d+)$', views.EventUpdate.as_view(), name='event_edit'),
]

