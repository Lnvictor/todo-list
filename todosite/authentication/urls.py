from django.contrib import admin
from django.urls import path
from .views import (
    home,
    get_sign_up,
    sign_sucessfull,
    get_login,
    validate_login,
    set_logout,
    login_fail,
    passwd_recovery,
    set_change_in_password,
)

app_name = "authentication"

urlpatterns = [
    path("sign-up/", get_sign_up, name="sign-up"),
    path("login/", get_login, name="login"),
    path("login-failed/", login_fail, name="login-failed"),
    path("logout/", set_logout, name="logout"),
    path("login-validation/", validate_login, name="login_validation"),
    path("sign-up-success/", sign_sucessfull, name="sign_successfull"),
    path("passwd-recovery/", passwd_recovery, name="passwd-recovery"),
    path(
        "set-change-password/",
        set_change_in_password,
        name="set-change-password",
    ),
]
