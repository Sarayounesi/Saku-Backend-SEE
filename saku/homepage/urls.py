from django.urls import path
from .views import HomepageView

app_name = "homepage"
urlpatterns = [
    path("<int:year>", HomepageView.as_view(), name="homepage"),
]
