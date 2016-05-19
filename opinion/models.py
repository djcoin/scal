from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone


from operator import attrgetter
from event import models as mevent

from taggit.managers import TaggableManager


# Todo: taggable manager: should add a description to what that is?!


# Todo: create an external channel/comment

class Rating(models.Model):
    "Rate some event element"
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    element = models.ForeignKey(mevent.Element)

    authenticity = models.FloatField()
    interest = models.FloatField()

    text = models.TextField("explanation")



class Hypothesis(models.Model):
    """From a some fact, explain a subject: more than a tag?"""
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")

    text = models.TextField("")

    elements = models.ManyToManyField(mevent.Element)
    events = models.ManyToManyField(mevent.Event)

    tags = TaggableManager()

    def get_rating(self):
        elems = self.elements.values_list('rating', flat=True)
        return [sum(elems), len(elems)]


    def save(self, **kwargs):
        self.touch(self.modified_by, commit=False)
        super(Hypothesis, self).save(**kwargs)


    def touch(self, user, commit=True):
        if not self.pk:
            self.created_by = self.modified_by
            self.modified = timezone.now()

        self.modified = timezone.now()
        if commit:
            self.save()




# class Opinion(models.Model):
#     """Analysis made by a user"""
#     text = models.TextField("")
#     tags = TaggableManager()


# https://docs.djangoproject.com/fr/1.9/ref/models/fields/#django.db.models.ManyToManyField



