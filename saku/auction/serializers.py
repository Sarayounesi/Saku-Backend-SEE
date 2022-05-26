import logging
import random
import string
from rest_framework import serializers
from auction.models import Auction, Tags
from user_profile.serializers import GeneralProfileSerializer
from bid.models import Bid


def get_random_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))


class CreateAuctionRequestSerializer(serializers.ModelSerializer):
    # tags = serializers.ListSerializer(child=serializers.CharField(), required=False)

    class Meta:
        model = Auction
        exclude = ('token',)

    def validate(self, data):
        if data["finished_at"] <= data["created_at"]:
            raise serializers.ValidationError("created_at can't be greater or equal to finished_at")
        return super().validate(data)

    def create(self, validated_data):
        token = get_random_token()
        tag_names = validated_data.get('tags')
        tags = []
        if tag_names:
            for tag in tag_names:
                tag_instance, _ = Tags.objects.get_or_create(name=tag)
                tags.append(tag_instance)
        validated_data['tags'] = tags
        while Auction.objects.filter(token=token).exists():
            token = get_random_token()
        validated_data['token'] = token
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class GetAuctionRequestSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    user = GeneralProfileSerializer()
    best_bid = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = ('name', 'token', 'user', 'created_at', 'finished_at',
                  'mode', 'limit', 'location', 'description', 'is_private',
                  'category', 'tags', 'participants_num', 'show_best_bid', 'best_bid')

    def get_best_bid(self, obj):
        bids = Bid.objects.filter(auction=obj.id).order_by('price')
        if len(bids)>0:
            if obj.mode == 1:
                best_bid = bids.last()
            else:
                best_bid = bids.first()
            user_data = GeneralProfileSerializer(best_bid.user).data
            return {"user":user_data, "time":best_bid.time, "price":best_bid.price}
        return {}
