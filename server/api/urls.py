from django.urls import path
from . import views

urlpatterns = [
    path("auth/login", views.auth.LoginView.as_view()),
    path("auth/logout", views.auth.LogoutView.as_view()),
    path("auth/change_password", views.auth.ChangePasswordView.as_view()),
    path("auth/apikeys/generate", views.auth.GenerateAPIKeyView.as_view()),
    path("auth/apikeys/check", views.auth.CheckAPIKeyView.as_view()),
    path("records/list", views.records.ListRecordsView.as_view()),
    path("records/create", views.records.CreateRecordView.as_view()),
    path("records/id/<str:id>", views.records.RetrieveRecordView.as_view()),
    path("records/journal/create", views.records.journal.CreateJournalAccomplishmentsView.as_view()),
    path("records/journal/list", views.records.journal.ListJournalAccomplishmentsView.as_view()),
    path("users/self", views.users.SelfView.as_view()),
]
