from rest_framework.generics import ListAPIView
from chat.models import Chat, Message
from user_profile.models import Profile
# Create your views here.
from rest_framework.permissions import IsAuthenticated
from chat.serializers import GetChatSerializer, GetMessageSerializer
from rest_framework.response import Response


def _get_chat_by_username(starter_username, contact_username):
    user_names = sorted([starter_username, contact_username])
    return Chat.objects.get(token="-".join(user_names))


class GetChat(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetChatSerializer

    def get_queryset(self):
        chats = []
        raw_chats = Chat.objects.values("created_at", "token").order_by("-created_at")
        for c in raw_chats:
            usernames = c["token"].split("-")
            if self.request.user.username in usernames:
                c["username"] = usernames[
                    1 - usernames.index(self.request.user.username)
                ]
                c["profile_image"] = Profile.objects.get(user__username=c["username"]).profile_image
                chats.append(c)
        return chats

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.get_queryset(), many=True)
        if serializer.is_valid():
            return Response(data=serializer.data, status=200)
        # Todo: Fix this
        raise


class GetMessage(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetMessageSerializer
    chat = None

    def get_queryset(self):
        return list(
            Message.objects.filter(chat=self.chat)
            .values("sender", "text", "created_at")
            .order_by("-created_at")
        )

    def get(self, request, *args, **kwargs):
        self.chat = _get_chat_by_username(
            self.request.user.username, kwargs["username"]
        )
        serializer = self.get_serializer(data=self.get_queryset(), many=True)
        if serializer.is_valid():
            return Response(data=serializer.data, status=200)
        # Todo: Fix this
        raise
