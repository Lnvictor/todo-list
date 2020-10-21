from django.contrib import admin
from django.urls import path
from .views import (
    home,
    new_task,
    new_issue,
    delete_task,
    change_status_of_task,
    change_status_of_issue,
    delete_issue,
)

app_name = "base"

urlpatterns = [
    path("", home, name="home"),
    path("new-task/", new_task, name="new-task"),
    path("new-issue/<int:pk>/", new_issue, name="new-issue"),
    path("delete-task/<int:pk>", delete_task, name="delete"),
    path(
        "change-status/<int:pk>/",
        change_status_of_task,
        name="change_status",
    ),
    path(
        "change-status-issue/<int:pk>/",
        change_status_of_issue,
        name="change_status_of_issue",
    ),
    path("delete-task/<int:pk>/", delete_issue, name="delete_issue"),
]
