from django.urls import path, include
from .views import get_profile, delete_account


app_name = "user_profile"

urlpatterns = [
    path("", get_profile, name="profile-index"),
    path(
        "delete-account/<str:username>/", delete_account, name="delete-account"
    ),
]
