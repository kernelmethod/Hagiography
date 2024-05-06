from django.urls import path
from . import views

urlpatterns = [path("records/list", views.records.ListRecords.as_view())]
