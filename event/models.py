from __future__ import unicode_literals

from functools import partial

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager


# https://github.com/pinax/pinax-documents/blob/master/pinax/documents/models.py
# https://docs.djangoproject.com/fr/1.9/ref/models/fields/#foreignkey

class Event(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")


    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField("when")
    # parent = models.ForeignKey('self', on_delete=models.SET_NULL)

    # duration..?

    tags = TaggableManager()


    def save(self, **kwargs):
        self.touch(self.modified_by, commit=False)
        super(Event, self).save(**kwargs)


    def touch(self, user, commit=True):
        if not self.pk:
            self.created_by = self.modified_by
            self.modified = timezone.now()

        self.modified = timezone.now()
        if commit:
            self.save()

    def get_absolute_url(self):
        return reverse('index')
        # return reverse('event-detail', kwargs={'pk': self.pk})


# https://docs.djangoproject.com/fr/1.9/ref/models/fields/#manytomanyfield

# https://docs.djangoproject.com/fr/1.9/topics/db/models/#model-inheritance


# https://github.com/bradleyg/django-s3direct



# One element
# One element are grouped on one event
# one event is divided into multiple other events
# what is the link? parental?





class Element(models.Model):
    """
    This element is subject to discussion.
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")
    created = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="+")

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField("when")

    #
    authenticity = models.FloatField()
    interest = models.FloatField()

    #
    tags = TaggableManager()


    def save(self, **kwargs):
        self.touch(self.modified_by, commit=False)
        super(Element, self).save(**kwargs)


    def touch(self, user, commit=True):
        if not self.pk:
            self.created_by = self.modified_by
            self.modified = timezone.now()

        self.modified = timezone.now()
        if commit:
            self.save()




def user_directory_path(pfx, instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return '{0}/user_{1}/{2}'.format(pfx, instance.user.id, filename)



# url and upload could be multiple or a torrent or something

class Video(Element):
    url = models.URLField(blank=True, null=True)
    upload = models.FileField(upload_to=partial(user_directory_path, 'vids'), blank=True, null=True)


class Image(Element):
    url = models.URLField(blank=True, null=True)
    upload = models.FileField(upload_to=partial(user_directory_path, 'imgs'), blank=True, null=True)


class Sound(Element):
    url = models.URLField(blank=True, null=True)
    upload = models.FileField(upload_to=partial(user_directory_path, 'sounds'), blank=True, null=True)


class Article(Element):
    url = models.URLField(blank=True, null=True)
    # upload could be a zip

    # article is itself a bundle of element...
    # sound may be, video may be, etc.

