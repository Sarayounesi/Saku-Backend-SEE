import logging
import random
import string
from rest_framework import serializers
from auction.models import Auction, Tags


def get_random_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


class CreateAuctionRequestSerializer(serializers.ModelSerializer):
    tags = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Auction
        exclude = ('token',)

    def validate(self, data):
        if data["finished_at"] <= data["created_at"]:
            raise serializers.ValidationError("created_at can't be greater or equal to finished_at")
        return super().validate(data)

    def create(self, validated_data):
        token = get_random_token()
        tag_names = validated_data.pop('tags')
        tags = []
        for tag in tag_names:
            tag_instance, _ = Tags.objects.get_or_create(name=tag)
            tags.append(tag_instance)
        while Auction.objects.filter(token=token).exists():
            token = get_random_token()
        validated_data['token'] = token
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        exclude = ('id',)


class GetAuctionRequestSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Auction
        fields = '__all__'
