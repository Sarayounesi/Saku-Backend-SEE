import json
import jwt
from channels.consumer import AsyncConsumer
from channels import exceptions
from saku import settings
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from chat.models import Chat, Message


class ChatConsumer(AsyncConsumer):
    def __init__(self):
        self.chat = None
        self.contact_username = None
        self.token = None
        self.user = None

    def _get_user_id_by_jwt(self):
        sender_jwt = self.scope["url_route"]["kwargs"]["sender_jwt"]
        return jwt.decode(sender_jwt, key=settings.SECRET_KEY, algorithms=["HS256"])[
            "user_id"
        ]

    @database_sync_to_async
    def _get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def _is_user_exists(self, username):
        return User.objects.filter(username=username).exists()

    @database_sync_to_async
    def _get_chat(self, token):
        return Chat.objects.get_or_create(token=token)[0]

    @database_sync_to_async
    def _create_message(self, text, user):
        return Message.objects.create(text=text, chat=self.chat, sender=user)

    async def websocket_connect(self, event):
        self.user = await self._get_user_by_id(self._get_user_id_by_jwt())
        self.contact_username = self.scope["url_route"]["kwargs"]["username"]

        if not self.contact_username or not await self._is_user_exists(
            self.contact_username
        ):
            raise exceptions.DenyConnection

        usernames = sorted([self.user.username, self.contact_username])
        self.token = "-".join(usernames)

        if len(self.token) > 25:
            self.token = self.token[:25]

        self.chat = await self._get_chat(self.token)

        await self.channel_layer.group_add(self.token, self.channel_name)

        await self.send({"type": "websocket.accept"})

    async def websocket_disconnect(self, event):
        pass

    async def websocket_receive(self, event):
        await self._create_message(json.loads(event["text"])["message"], self.user)
        await self.channel_layer.group_send(
            self.token, {"type": "chat_message", "text": event["text"]}
        )

    async def chat_message(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})
