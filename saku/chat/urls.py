from django.urls import path
from chat.views import GetChat, GetMessage

urlpatterns = [
    path("my/", GetChat.as_view()),
    path("messages/<str:username>/", GetMessage.as_view()),
]
