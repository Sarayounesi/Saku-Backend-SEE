from django.urls import path
from .views import UpdateProfile, DeleteProfilePicture

app_name = "user_profile"
urlpatterns = [
    path("update/", UpdateProfile.as_view(), name="update_profile"),
    path(
        "delete/picture/", DeleteProfilePicture.as_view(), name="delete_profile_image"
    ),
]
