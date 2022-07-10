from django.urls import path
from auction.consumers import AuctionConsumer

auction_websocket_urlpatterns = [
    path("auction/<str:token>/<str:sender_jwt>", AuctionConsumer.as_asgi())
]
