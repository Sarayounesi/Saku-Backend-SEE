import random
import string
from rest_framework import serializers
from user_profile.serializers import GeneralProfileSerializer
from bid.models import Bid
from auction.models import Auction, Tags, Category


def get_random_token():
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(8)
    )


class CreateAuctionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        exclude = ("token", "celery_task_id")

    def validate(self, data):
        if data["finished_at"] <= data["created_at"]:
            raise serializers.ValidationError(
                "created_at can't be greater or equal to finished_at"
            )
        return super().validate(data)

    def create(self, validated_data):
        token = get_random_token()
        while Auction.objects.filter(token=token).exists():
            token = get_random_token()
        validated_data["token"] = token
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"


class GetAuctionRequestSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    user = GeneralProfileSerializer()
    best_bid = serializers.SerializerMethodField()

    class Meta:
        model = Auction
        fields = (
            "name",
            "token",
            "user",
            "created_at",
            "finished_at",
            "mode",
            "limit",
            "location",
            "description",
            "is_private",
            "category",
            "tags",
            "participants_num",
            "show_best_bid",
            "best_bid",
            "auction_image",
            "is_online"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].context.update(self.context)

    def get_serializer_context(self):
        context = {"request": self.context.get("request")}
        return context

    def get_best_bid(self, obj):
        # best_bid = obj.best_bid
        # if best_bid == None:
        bids = Bid.objects.filter(auction=obj.id).order_by("price")
        if len(bids) > 0:
            if obj.mode == 1:
                best_bid = bids.last()
            else:
                best_bid = bids.first()
        # if best_bid != None:
            user_data = GeneralProfileSerializer(
                best_bid.user, context={"request": self.context.get("request")}
            ).data
            return {"user": user_data, "time": best_bid.time, "price": best_bid.price}
        return {}


class GetCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UpdateAuctionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        exclude = ("token", "user")
        extra_kwargs = {
            "created_at": {"read_only": True},
            "mode": {"read_only": True},
            "limit": {"read_only": True},
            "is_private": {"read_only": True},
            "participants_num": {"read_only": True},
        }

    def validate(self, data):
        token = self.context["token"]
        auction = Auction.objects.filter(token=token)[0]
        created_at = auction.created_at
        if data.get("created_at"):
            created_at = data.get("created_at")
        finished_at = auction.finished_at
        if data.get("finished_at"):
            finished_at = data.get("finished_at")

        if finished_at <= created_at:
            raise serializers.ValidationError(
                "created_at can't be greater or equal to finished_at"
            )
        return super().validate(data)
