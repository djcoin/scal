# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
from django.contrib import admin
from .models import Organizer, Person, Location, Event


class AdminSaveAsRedirect(admin.ModelAdmin):
    """Add a save_as button but redirect on the change page after save"""
    save_as = True

    def response_add(self, request, obj, post_url_continue=None):
        if '_saveasnew' in request.POST:
            request.POST["_continue"] = True

        return super(AdminSaveAsRedirect, self).response_add(request, obj, post_url_continue)


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
        pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
        pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
        pass


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



@admin.register(Event)
class EventAdmin(AdminSaveAsRedirect):
    fields = fields + ['poster', 'poster_tag', 'landscape', 'landscape_tag'] # 'json_tag' ]
    readonly_fields = ['poster_tag', 'landscape_tag'] # 'json_tag')

    list_display = ('name', 'start', 'end', 'get_city' )
