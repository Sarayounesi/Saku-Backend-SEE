import datetime

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from auction.models import Auction
from bid.serializers import BidSerializer
from bid.models import Bid


class ListCreateAuctionBid(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidSerializer
    filterset_fields = ('user', 'auction')
    ordering_fields = ('time', 'price')

    def post(self, request, token):
        auction = get_object_or_404(Auction, token=token)
        request.data['user'] = request.user.id
        request.data['auction'] = auction.id
        request.data['time'] = datetime.datetime.now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bid = serializer.save()
        if len(Bid.objects.filter(user=bid.user.id, auction=bid.auction.id)) == 1:
            auction.participants_num += 1
            auction.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        token = self.kwargs['token']
        auction = get_object_or_404(Auction, token=token)
        return Bid.objects.filter(auction=auction)


class UserBidsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidSerializer
    filterset_fields = ('auction',)
    ordering_fields = ('time', 'price')

    def get_queryset(self):
        user = self.request.user
        return Bid.objects.filter(user=user)


class UserAuctionBidsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BidSerializer
    ordering_fields = ('time', 'price')

    def get_queryset(self):
        user = self.request.user
        token = self.kwargs['token']
        auction = get_object_or_404(Auction, token=token)
        return Bid.objects.filter(user=user, auction=auction)