
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    # url(r'^edit$', views.EditView.as_view(), name="event-edit")
    url(r'^create$', views.CreateView.as_view(), name="event-create")
]

