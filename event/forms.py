from __future__ import unicode_literals

from django import forms
from .models import Event

from django.forms import ModelForm
from .models import Event, Location, Organizer, Person
from datetimewidget.widgets import DateTimeWidget, DateWidget

from dal import autocomplete



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


# https://django-autocomplete-light.readthedocs.io/en/master/index.html
# https://django-autocomplete-light.readthedocs.io/en/master/tutorial.html#create-an-autocomplete-view
# http://stackoverflow.com/questions/18828337/django-autocomplete-light-filter-queryset

class EventForm(ModelForm):

    class Meta:
        model = Event
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['location'] = forms.ModelChoiceField(
            queryset=Location.objects.all(),
            widget=autocomplete.ModelSelect2(url='event:autocomplete-location')
        )
        self.fields['attendees'] = forms.ModelMultipleChoiceField(
            queryset=Person.objects.all(),
            widget=autocomplete.ModelSelect2Multiple(url='event:autocomplete-person')
        )
        self.fields['organizers'] = forms.ModelMultipleChoiceField(
            queryset=Organizer.objects.all(),
            widget=autocomplete.ModelSelect2Multiple(url='event:autocomplete-organizer')
        )

