# -*- coding: utf-8 -*- 

from __future__ import unicode_literals

import json

from django.db import models

from django.template.defaultfilters import date
import datetime

from django.utils.translation import ugettext, ugettext_lazy as _




class Organizer(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True, default="")
    facebook = models.URLField(blank=True, default="")

    def __str__(self):
        return self.name


class Location(models.Model):
    city = models.CharField(max_length=20)
    area = models.CharField(max_length=50)
    building = models.CharField(max_length=20)
    address = models.CharField(max_length=200)


class Person(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.name


# class EventType(models.Model):
# class EventSubject(models.Model):

_event_type_choices = (
    ('salon', 'salon'),
    ('manifestation', 'manifestation'),
    ('dedicace', 'dedicace'),
    ('radio/mumble', 'radio/mumble'),
    ('emission TV', 'emission TV'),
    ('conference', 'conference'),
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

    def __str__(self):
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


    def __str__(self):
        return self.name


    def poster_tag(self):
        return u'<img src="%s" />' % self.poster

    poster_tag.short_description = 'Poster image'
    poster_tag.allow_tags = True


    def landscape_tag(self):
        return u'<img src="%s" />' % self.landscape

    landscape_tag.short_description = 'Landscape image'
    landscape_tag.allow_tags = True

    def json_tag(self):
        return u'<pre>' + self.as_json() + '</pre>'

    json_tag.short_description = 'json look'
    json_tag.allow_tags = True


    def prepare_json(self):
        d = {}
        for x in ['name', 'event_type', 'event_subject', 'website', 'facebook',
                  'reg_price', 'reg_type', 'reg_email', 'reg_website', 'reg_facebook']:
            d[x] = getattr(self, x)

        for x in ['start', 'end']:
            d[x] = getattr(self, x)


        # print(self.organizers.all())

        orgs = [{'name': o.name,
                 'website': o.website,
                 'facebook': o.facebook}
                 for o in self.organizers.all()]

        attendees = [{'name': p.name, 'description': p.description} for p in self.attendees.all()]

        d['attendees'] = attendees
        d['organizers'] = orgs

        d['poster'] = str(self.poster)
        d['landscape'] = str(self.landscape)

        return d


    def as_json(self, indent=4):
        return json.dumps(self.prepare_json(), indent=indent)



# start time
# end time
# duration


# class Images(models.Model):


"""

:cal
[
{
:date
[
"2016-01-01"
]
:name
"My event"
:event
"conference"
:category
[
:geopolitic
]
:start-time
"18:00"
:end-time
"19:30"
}
{
:date
[
"2016-01-02"
]
:name
"My event 2"
:event
"conference"
:category
[
:economic
]
:start-time
"19:15"
:end-time
"20:30"
}
{
:date
[
"2016-01-07"
]
:name
"Conf geo"
:event
"conference"
:category
[
:geopolitic
]
:start-time
"16:30"
:end-time
"18:00"
:template
"**Bonjour ceci est un test!** {{start-time}}"
}
]
:events
[
{
:date
[
"2016-01-01"
]
:name
"My event"
:event
"conference"
:category
[
:geopolitic
]
:start-time
"18:00"
:end-time
"19:30"
}
{
:date
[
"2016-01-02"
]
:name
"My event 2"
:event
"conference"
:category
[
:economic
]
:start-time
"19:15"
:end-time
"20:30"
}
{
:date
[
"2016-01-07"
]
:name
"Conf geo"
:event
"conference"
:category
[
:geopolitic
]
:start-time
"16:30"
:end-time
"18:00"
:template
"**Bonjour ceci est un test!** {{start-time}}"
}
]
:categories
[
{
:type
:geopolitic
:text
"Géopolitique"
:color
"#4100FF"
}
{
:type
:politic
:text
"Politique"
:color
"#2481eb"
}
{
:type
:economic
:text
"Économie"
:color
"#00ecb9"
}
{
:type
:ecologic
:text
"Écologie"
:color
"#00e253"
}
{
:type
:alternative
:text
"Alternatives"
:color
"#f9ff00"
}
{
:type
:media
:text
"Média"
:color
"#ffb800"
}
{
:type
:history
:text
"Histoire"
:color
"#ff0000"
}
{
:type
:spirituality
:text
"Spiritualité"
:color
"#ff00be"
}
{
:type
:culture
:text
"Culture"
:color
"#ae00f0"
}
]
:filter
nil
:view
{
:date-range
#{
"2015-12-28" "2015-12-29" "2015-12-30" "2015-12-31" "2016-01-01" "2016-01-02" "2016-01-03"
}
}
"""


