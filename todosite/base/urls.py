from django.contrib import admin
from django.urls import path
from .views import (
    home,
    new_task,
    new_issue,
    remove_task,
    change_status_of_task,
)

app_name = "base"

urlpatterns = [
    path("", home, name="home"),
    path("new-task/", new_task, name="new-task"),
    path("new-issue/<str:task_name>/", new_issue, name="new-issue"),
    path("delete-task/<str:name>", remove_task, name="delete"),
    path(
        "change-status/<str:name>",
        change_status_of_task,
        name="change_status",
    ),
]
