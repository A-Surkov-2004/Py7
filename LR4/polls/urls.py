from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from . import views

from django.contrib.auth.decorators import login_required

app_name = "polls"
urlpatterns = [
    path("", login_required(views.IndexView.as_view()), name="index"),
    path("<int:pk>/", login_required(views.DetailView.as_view()), name="detail"),
    path("<int:pk>/results/", login_required(views.ResultsView.as_view()), name="results"),
    path("<int:question_id>/vote/", login_required(views.vote), name="vote"),
    path("new_poll/", login_required(views.NewPollView.as_view()), name="new_poll"),
]