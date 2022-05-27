from django.urls import path
from auction.views import CreateListAuction, CategoryList, DetailedAuction

urlpatterns = [
    path('', CreateListAuction.as_view(), name="auction"),
    path('categories/', CategoryList.as_view()),
    path('<str:token>', DetailedAuction.as_view(), name="detailed_auction"),
]