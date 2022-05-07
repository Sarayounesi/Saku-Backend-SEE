from django.db.models import Max
from rest_framework import serializers

from auction.models import Auction
from bid.models import Bid


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        exclude = ('id',)

    def validate(self, data):
        price = data.get('price')
        time = data.get('time')
        auction = data.get('auction').id

        auction_finished = Auction.objects.get(id=auction).finished_at

        if auction_finished < time:
            raise serializers.ValidationError("bid cannot get created for finished auctions.")
        
        bids = Bid.objects.filter(auction=auction)
        max_price = 0
        if len(bids) > 0:
            max_price = bids.aggregate(Max('price')).get('price__max')
        
        if max_price > price:
            raise serializers.ValidationError("bigger bid on this auction already exists.")

        return data
