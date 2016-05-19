from __future__ import unicode_literals

from django import forms
from .models import (Event, Element)



# https://github.com/pinax/pinax-documents/blob/master/pinax/documents/forms.py
# http://stackoverflow.com/questions/6355258/custom-form-author-auto-save-author-to-db

# https://docs.djangoproject.com/fr/1.9/topics/class-based-views/
# https://docs.djangoproject.com/fr/1.9/topics/class-based-views/generic-editing/


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('created_by', 'created', 'modified', 'modified_by')

    def __init__(self, *args, **kwargs):
        super(TrackerForm, self).__init__(*args, **kwargs)




