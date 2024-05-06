from django.urls import path
from . import views

urlpatterns = [
    path("auth/login", views.auth.LoginView.as_view()),
    path("records/list", views.records.ListRecords.as_view()),
]
