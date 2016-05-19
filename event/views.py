from django.shortcuts import render


from django.http import HttpResponse

# https://github.com/pinax/pinax-documents/blob/master/pinax/documents/views.py

from account.mixins import LoginRequiredMixin


from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    TemplateView,
)


class IndexView(LoginRequiredMixin, TemplateView):

    template_name = "event/index.html"

    def get_context_data(self, **kwargs):
        ctx = kwargs
        return ctx


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")



class CreateView(LoginRequiredMixin, TemplateView):

    template_name = "event/create.html"


    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super(CreateView, self).form_valid(form)


class EditView(LoginRequiredMixin, TemplateView):

    template_name = "event/edit.html"


