from django.urls import path
from bid.views import ListCreateAuctionBid, UserBidsView

app_name = 'bid'
urlpatterns = [
    path('<str:token>', ListCreateAuctionBid.as_view(), name="list_create_bid"),
    path('', UserBidsView.as_view(), name="get_user_bids"),
]