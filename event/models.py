# -*- coding: utf-8 -*- 

from __future__ import unicode_literals

import json

from django.db import models

from django.template.defaultfilters import date
import datetime

from django.utils.translation import ugettext, ugettext_lazy as _


class Location(models.Model):
    city = models.CharField(max_length=20)
    area = models.CharField(blank=True, default="", max_length=50)
    building = models.CharField(blank=True, default="", max_length=20)
    address = models.CharField(max_length=200)
    url = models.URLField(blank=True, default="")

    def __unicode__(self):
        return self.address + ' (' + self.city + ')'


class Organizer(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, default="")
    facebook = models.URLField(blank=True, default="")
    image = models.FileField(blank=True, upload_to='uploads/')

    def __unicode__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    image = models.FileField(blank=True, upload_to='uploads/')

    def __unicode__(self):
        return self.name


# class EventType(models.Model):
# class EventSubject(models.Model):

_event_type_choices = (
    ('salon' , u"Salon"),
    ('manifestation' , u"Manifestation"),
    ('dedicace' , u"Dédicace"),
    ('mumble' , u"Mumble"),
    ('emission TV' , u"Émission TV"),
    ('conference' , u"Conférence"),
    ('theatre' , u"Théatre"),
    ('cinema' , u"Cinéma"),
    ('emission-radio' , u"Émission radio"),
)

_event_subject_choices = (
    ('geopolitic', 'géopolitique'),
    ('politic', 'politique'),
    ('economy', 'économie'),
    ('ecology', 'écologie'),
    ('alternative', 'alternative'),
    ('media', 'média'),
    ('history', 'histoire'),
    ('spirituality', 'spiritualité'),
    ('culture', 'cultures'),
    ('science', 'sciences'),
)


class EventBase(models.Model):
    '''
    This model stores meta data for a date.  You can relate this data to many
    other models.
    '''

    class Meta:
        abstract = True

    name = models.CharField(_("title"), max_length=255)

    start = models.DateTimeField(_("start"))
    end = models.DateTimeField(_("end"), help_text=_("The end time must be later than the start time."))
    # creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name=_("creator"),
    #                             related_name='creator')
    created_on = models.DateTimeField(_("created on"), auto_now_add=True)
    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    # rule = models.ForeignKey(Rule, null=True, blank=True, verbose_name=_("rule"),
    #                          help_text=_("Select '----' for a one time only event."))
    # end_recurring_period = models.DateTimeField(_("end recurring period"), null=True, blank=True,
    #                                             help_text=_("This date is ignored for one time only events."))
    # calendar = models.ForeignKey(Calendar, null=True, blank=True, verbose_name=_("calendar"))
    # objects = EventManager()

    def __unicode__(self):
        return ugettext('%(name)s: %(start)s - %(end)s') % {
            'title': self.title,
            'start': date(self.start, django_settings.DATE_FORMAT),
            'end': date(self.end, django_settings.DATE_FORMAT),
        }




class Event(EventBase):


    # name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=_event_type_choices)
    event_subject = models.CharField(max_length=20, choices=_event_subject_choices)

    website = models.URLField(blank=True, default="")
    facebook = models.URLField(blank=True, default="")

    # registration
    reg_price = models.CharField(max_length=300, blank=True, default="")
    reg_type = models.CharField(max_length=100, blank=True, default="")
    reg_email = models.CharField(max_length=50, blank=True, default="")
    reg_website = models.URLField(blank=True, default="")
    reg_facebook = models.URLField(blank=True, default="")

    poster = models.FileField(blank=True, upload_to='uploads/')
    landscape = models.FileField(blank=True, upload_to='uploads/')

    organizers = models.ManyToManyField(Organizer, blank=True)
    attendees = models.ManyToManyField(Person, blank=True)

    # TODO: remove null
    location = models.ForeignKey(Location, null=True, blank=True, verbose_name=_("location"))

    description = models.TextField(blank=True, default="")

    def __unicode__(self):
        return self.name


    def poster_tag(self):
        return u'<img src="%s" />' % self.poster.url

    poster_tag.short_description = 'Poster image'
    poster_tag.allow_tags = True


    def landscape_tag(self):
        return u'<img src="%s" />' % self.landscape.url

    landscape_tag.short_description = 'Landscape image'
    landscape_tag.allow_tags = True

    def json_tag(self):
        return u'<pre>' + self.as_json() + '</pre>'

    json_tag.short_description = 'json look'
    json_tag.allow_tags = True


    def get_city(self):
        return self.location.city if self.location else None

    get_city.short_description = 'City'
    get_city.admin_order_field = 'location__city'


    def prepare_json(self):
        d = {}
        for x in ['name', 'event_type', 'event_subject', 'website', 'facebook',
                  'reg_price', 'reg_type', 'reg_email', 'reg_website', 'reg_facebook', 'description']:
            d[x] = getattr(self, x)

        for x in ['start', 'end']:
            d[x] = getattr(self, x)


        d['id'] = self.pk
        d['poster'] = self.poster.url if self.poster else None
        d['landscape'] = self.landscape.url if self.landscape else None

        orgs = [{'name': o.name,
                 'website': o.website,
                 'facebook': o.facebook}
                 for o in self.organizers.all()]

        attendees = [{'name': p.name, 'description': p.description} for p in self.attendees.all()]

        d['attendees'] = attendees
        d['organizers'] = orgs

        if self.location:
            d['location'] = {'city': self.location.city,
                             'area': self.location.area,
                             'building': self.location.building,
                             'address': self.location.address,
                             'url': self.location.url}
        else:
            d['location'] = None


        return d


    def as_json(self, indent=4):
        return json.dumps(self.prepare_json(), indent=indent)



# start time
# end time
# duration


# class Images(models.Model):


