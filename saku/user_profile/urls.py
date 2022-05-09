from django.urls import path
from .views import UpdateProfile

app_name = "user_profile"
urlpatterns = [
    path("update/", UpdateProfile.as_view(), name="update_profile")
]