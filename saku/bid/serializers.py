from django.db.models import Max
from rest_framework import serializers
from auction.models import Auction
from bid.models import Bid


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        exclude = ('id',)
        extra_kwargs = {
            "price": {"required": True}
        }

    def validate(self, data):
        user = data.get('user')
        price = data.get('price')
        time = data.get('time')
        auction_id = data.get('auction').id
        auction = Auction.objects.get(id=auction_id)

        #check auction owner:
        if auction.user == user:
            raise serializers.ValidationError("Auction owners cannot bids for their auctions.")

        #check auction finished at:
        auction_finished = auction.finished_at
        if auction_finished < time:
            raise serializers.ValidationError("Users cannot bid for finished auctions.")

        #check auction limit:
        auction_limit = auction.limit
        auction_mode = auction.mode
        if auction_mode == 1:
            if price < auction_limit:
                raise serializers.ValidationError("Users cannot bid lower than auction limit.")
        else:
            if price > auction_limit:
                raise serializers.ValidationError("Users cannot bid higher than auction limit.")

        #check auction is_private, mode:
        auction_private = auction.is_private
        if not auction_private:
            bids = Bid.objects.filter(auction=auction)
            if auction_mode == 1:
                max_price = auction_limit - 1
                if len(bids) > 0:
                    max_price = bids.aggregate(Max('price')).get('price__max')
                if max_price >= price:
                    raise serializers.ValidationError("Higher bid for this auction already exists.")
            else:
                min_price = auction_limit + 1
                if len(bids) > 0:
                    min_price = bids.aggregate(Min('price')).get('price__min')
                if min_price <= price:
                    raise serializers.ValidationError("Lower bid for this auction already exists.")
        return data
