from django.shortcuts import render


from django.http import HttpResponse

# https://github.com/pinax/pinax-documents/blob/master/pinax/documents/views.py

from account.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


from .forms import CreateEventForm
from .models import Event


from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)


class EventCreate(LoginRequiredMixin, CreateView):
    model = Event
    form_class = CreateEventForm
    success_url = reverse_lazy('event:event_list')

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super(EventCreate, self).form_valid(form)


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = CreateEventForm
    success_url = reverse_lazy('event:event_list')

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super(EventUpdate, self).form_valid(form)


class EventList(LoginRequiredMixin, ListView):
    model = Event
    success_url = reverse_lazy('event:event_list')



