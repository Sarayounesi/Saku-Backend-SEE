from rest_framework.serializers import Serializer, CharField, DateTimeField

class GetChatSerializer(Serializer):
    username = CharField(required=True)
    created_at = DateTimeField(required=True)
    profile_image = CharField(allow_null=True)

    class Meta:
        fields = ("created_at", "username", "profile_image")


class GetMessageSerializer(Serializer):
    text = CharField(required=True)
    sender = CharField(required=True)
    created_at = DateTimeField(required=True)

    class Meta:
        fields = ("text", "sender", "created_at")
