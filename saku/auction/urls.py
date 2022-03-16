from django.urls import path
from auction.views import CreateAuction

urlpatterns = [
    path('', CreateAuction.as_view()),
]