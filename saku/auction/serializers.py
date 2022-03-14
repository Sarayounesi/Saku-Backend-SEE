import random
import string
from rest_framework import serializers
from auction.models import Auction


def get_random_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


class CreateAuctionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        exclude = ('token',)

    def validate(self, data):
        if data["finished_at"] <= data["created_at"]:
            raise serializers.ValidationError("created_at can't be greater or equal to finished_at")
        return super().validate(data)

    def create(self, validated_data):
        token = get_random_token()
        while Auction.objects.filter(token=token).exists():
            token = get_random_token()
        validated_data['token'] = token
        return super().create(validated_data)
