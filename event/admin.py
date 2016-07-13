# -*- coding: utf-8 -*- 

from __future__ import unicode_literals
from django.contrib import admin
from .models import Organizer, Person, Event


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
        pass


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
        pass


fields = [
    'name', 'start', 'end',
    'event_type', 'event_subject', 'website', 'facebook',
    'reg_price', 'reg_type', 'reg_email', 'reg_website', 'reg_facebook',
    'organizers',
    'attendees'
]



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = fields + ['poster', 'poster_tag', 'landscape', 'landscape_tag', 'json_tag' ]
    readonly_fields = ('poster_tag', 'landscape_tag', 'json_tag')



