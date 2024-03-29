
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.EventList.as_view(), name="event_list"),
    url(r'^create$', views.EventCreate.as_view(), name="event_create"),
    url(r'^edit/(?P<pk>\d+)$', views.EventUpdate.as_view(), name='event_edit'),

    url(r'^widget/$', views.widget, name="event_widget"),
    url(r'^planning/$', views.planning, name="event_planning"),
    url(r'^cal/$', views.calendar, name="event_calendar"),

    url(r'^devcards/$', views.devcards, name="event_devcards"),
    url(r'^api/$', views.api, name="event_api"),

    url(r'^api/event/(?P<pk>\d+)$', views.api_event, name="event_api_detail"),

    url(r'^autocomplete/location',
        views.LocationAutocomplete.as_view(),
        name='autocomplete-location'),
    url(r'^autocomplete/organizer',
        views.OrganizerAutocomplete.as_view(),
        name='autocomplete-organizer'),
    url(r'^autocomplete/person',
        views.PersonAutocomplete.as_view(),
        name='autocomplete-person'),
]

