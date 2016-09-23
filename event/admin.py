# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
from django.contrib import admin
from .models import Organizer, Person, Location, Event
from .forms import EventForm


class AdminSaveAsRedirect(admin.ModelAdmin):
    """Add a save_as button but redirect on the change page after save"""
    save_as = True

    def response_add(self, request, obj, post_url_continue=None):
        if '_saveasnew' in request.POST:
            request.POST["_continue"] = True

        return super(AdminSaveAsRedirect, self).response_add(request, obj, post_url_continue)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ['name',]


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name',]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'area', 'building', 'address', 'url')
    search_fields = ['city','address']


fields = [
    'published',
    'name', 'start', 'end',
    'event_type', 'event_subject',
    'description', 'website', 'facebook',
    'reg_price', 'reg_type', 'reg_email', 'reg_website', 'reg_facebook',
    'organizers',
    'attendees',
    'location',
]


# http://stackoverflow.com/questions/4337304/django-admin-changing-the-widget-of-the-field-in-admin

@admin.register(Event)
class EventAdmin(AdminSaveAsRedirect):
    fields = fields + ['poster', 'poster_tag', 'landscape', 'landscape_tag'] # 'json_tag' ]
    readonly_fields = ['poster_tag', 'landscape_tag'] # 'json_tag')

    list_display = ('name', 'start', 'end', 'get_city' )

    search_fields = ['name', ]

    date_hierarchy = 'start'

    form = EventForm
    # https://gitlab.com/rosarior/awesome-django#admin-interface
    # https://pypi.python.org/pypi/django-searchable-select/0.8
    # http://stackoverflow.com/questions/5385933/a-better-django-admin-manytomany-field-widget
    # https://github.com/yourlabs/django-autocomplete-light

    # filter_horizontal = ('organizers', 'attendees')
