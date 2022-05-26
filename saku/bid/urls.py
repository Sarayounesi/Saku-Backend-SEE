from django.urls import path
from bid.views import ListCreateAuctionBid, UserBidsView, UserAuctionBidsView

app_name = 'bid'
urlpatterns = [
    path('<str:token>', ListCreateAuctionBid.as_view(), name="list_create_bid"),
    path('my/', UserBidsView.as_view(), name="get_user_bids"),
    path('my/<str:token>', UserAuctionBidsView.as_view(), name="user_auction_bids"),
]