from django.urls import path
from . import views

urlpatterns = [
    path("auth/login", views.auth.LoginView.as_view()),
    path("auth/change_password", views.auth.ChangePasswordView.as_view()),
    path("records/list", views.records.ListRecords.as_view()),
    path("users/self", views.users.SelfView.as_view()),
]
