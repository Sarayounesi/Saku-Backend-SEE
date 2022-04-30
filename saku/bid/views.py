import datetime

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from auction.models import Auction
from bid.serializers import BidSerializer
from bid.models import Bid

#TODO: add search and filter

class ListCreateAuctionBid(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer

    def post(self, request, token):
        auction = get_object_or_404(Auction, token=token)
        request.data['user'] = request.user.id
        request.data['auction'] = auction.id
        request.data['time'] = datetime.datetime.now()
        return super().post(request)

    def get_queryset(self):
        token = self.kwargs['token']
        auction = get_object_or_404(Auction, token=token)
        return Bid.objects.filter(auction=auction)


class UserBidsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidSerializer

    def get_queryset(self):
        user = self.request.user
        return Bid.objects.filter(user=user)
