from django.urls import path, include
from .views import get_profile, delete_account, change_username


app_name = "user_profile"

urlpatterns = [
    path("", get_profile, name="profile-index"),
    path("delete-account/<str:username>/", delete_account, name="delete-account"),
    path("change-username/<int:pk>/", change_username, name="change-username"),
]
