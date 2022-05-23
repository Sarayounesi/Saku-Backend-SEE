from django.urls import path
from auction.views import CreateListAuction, DetailedAuction

urlpatterns = [
    path('', CreateListAuction.as_view(), name="auction"),
    path('<str:token>', DetailedAuction.as_view(), name="detailed_auction"),
]