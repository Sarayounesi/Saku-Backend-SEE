from django.urls import path
from chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('chat/<str:username>/<str:sender_jwt>', ChatConsumer.as_asgi())
]
