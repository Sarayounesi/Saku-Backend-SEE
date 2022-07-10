import json
import jwt
from channels.consumer import AsyncConsumer
from saku import settings
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from auction.models import Auction
from bid.models import Bid


class AuctionConsumer(AsyncConsumer):
    def __init__(self):
        self.auction = None
        self.token = None
        self.user = None
        self.bid = None

    def _get_user_id_by_jwt(self):
        sender_jwt = self.scope["url_route"]["kwargs"]["sender_jwt"]
        return jwt.decode(sender_jwt, key=settings.SECRET_KEY, algorithms=["HS256"])[
            "user_id"
        ]

    @database_sync_to_async
    def _get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def _get_auction(self, token):
        return Auction.objects.get(token=token)

    @database_sync_to_async
    def _create_bid(self, price):
        return Bid.objects.create(price=price, auction=self.auction, user=self.user)

    async def websocket_connect(self, event):
        self.user = await self._get_user_by_id(self._get_user_id_by_jwt())
        self.token = self.scope["url_route"]["kwargs"]["token"]

        self.auction = await self._get_auction(self.token)

        await self.channel_layer.group_add(self.token, self.channel_name)

        await self.send({"type": "websocket.accept"})

    async def websocket_disconnect(self, event):
        pass

    async def websocket_receive(self, event):
        self.bid = await self._create_bid(int(json.loads(event["text"])["price"]))
        event["text"] = json.dumps(
            {
                "price": int(int(json.loads(event["text"])["price"])),
                "created_at": self.bid.time,
                "user": self.bid.user,
            },
            indent=4,
            sort_keys=True,
            default=str,
        )
        await self.channel_layer.group_send(
            self.token, {"type": "chat_message", "text": event["text"]}
        )

    async def chat_message(self, event):
        await self.send({"type": "websocket.send", "text": event["text"]})
