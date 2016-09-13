
import json, datetime
from django.shortcuts import render, get_object_or_404


# https://docs.djangoproject.com/fr/1.9/ref/request-response/


from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest


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



def widget(req):
    return render(req, 'widget.html')

def planning(req):
    return render(req, 'planning.html')

def calendar(req):
    return render(req, 'calendar.html')


def devcards(req):
    return render(req, 'devcards.html')


def to_date(s):
    "Date format: YYYY-MM-DD"
    return datetime.datetime.strptime(s, "%Y-%m-%d")

def api(req):
    """
    Get events from start to end, eg:
        http://localhost:8000/event/api/?start=2016-07-20&end=2016-07-28
    """
    start = req.GET.get('start')
    end = req.GET.get('end')

    if not start or not end:
        return HttpResponseBadRequest("Missing start and end parameter")

    try:
        start = to_date(start)
        end = to_date(end)
    except ValueError:
        return HttpResponseBadRequest("Bad format for start and end, should be YYYY-MM-DD")

    print(u"%s to %s" % (start, end))


    js = [e.prepare_json() for e in Event.objects.filter(start__date__gte=start, end__date__lte=end).all()]

    # print(json.dumps(js))

    return JsonResponse(js, safe=False, json_dumps_params={"indent": 2})



def api_event(req, pk):
    "Api call for a specific event by id"
    event = get_object_or_404(Event, pk=int(pk))
    return JsonResponse(event.prepare_json(), safe=False, json_dumps_params={"indent": 2})


