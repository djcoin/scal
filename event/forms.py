from __future__ import unicode_literals

from django import forms
from .models import Event

from django.forms import ModelForm
from datetimewidget.widgets import DateTimeWidget, DateWidget



# https://github.com/pinax/pinax-documents/blob/master/pinax/documents/forms.py
# http://stackoverflow.com/questions/6355258/custom-form-author-auto-save-author-to-db

# https://docs.djangoproject.com/fr/1.9/topics/class-based-views/
# https://docs.djangoproject.com/fr/1.9/topics/class-based-views/generic-editing/


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('created_on', 'updated_on')
        widgets = {
        #Use localization and bootstrap 3
            # 'date': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
            'date': DateWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
        }


