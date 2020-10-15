from django.contrib import admin
from django.urls import path
from .views import (
    home,
    get_sign_up,
    sign_sucefull,
    get_login,
    validate_login,
    set_logout,
    new_task,
    new_issue,
    remove_task,
    login_fail,
    change_status_of_task,
)

app_name = "base"

urlpatterns = [
    path("", home, name="home"),
    path("sign-up/", get_sign_up, name="sign-up"),
    path("login/", get_login, name="login"),
    path("login-failed/", login_fail, name="login-failed"),
    path("login-validation/", validate_login, name="login_validation"),
    path("sign-up-success/", sign_sucefull, name="login_sucefull"),
    path("logout/", set_logout, name="logout"),
    path("new-task/", new_task, name="new-task"),
    path("new-issue/<str:name>/", new_issue, name="new-issue"),
    path("delete-task/<str:name>", remove_task, name="delete"),
    path(
        "change-status/<str:name>",
        change_status_of_task,
        name="change_status",
    ),
]
