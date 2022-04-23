from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from auction.serializers import CreateAuctionRequestSerializer, GetAuctionRequestSerializer
from rest_framework.response import Response
from saku.serializers import GeneralCreateResponseSerializer, GeneralErrorResponseSerializer
from rest_framework.permissions import AllowAny
from auction.models import Auction


class CreateListAuction(generics.ListCreateAPIView):
    permission_classes = (AllowAny,)  # TODO: change to IsAuthorized after auth has merged.
    queryset = Auction.objects.order_by('finished_at')

    @swagger_auto_schema(
        responses={201: GeneralCreateResponseSerializer,
                   400: GeneralErrorResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={201: GeneralCreateResponseSerializer,
                   400: GeneralErrorResponseSerializer},
    )
    def get(self, request, *args, **kwargs):
        auctions = self.get_queryset()
        serializer = GetAuctionRequestSerializer(auctions, many=True)
        return Response(serializer.data, status=200)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetAuctionRequestSerializer
        return CreateAuctionRequestSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code != 201:
            return super().finalize_response(request, response, args, kwargs)

        response = GeneralCreateResponseSerializer(data={'status_code': 201, 'message': 'Created!'})
        if response.is_valid():
            return super().finalize_response(request, Response(response.data, status=201), args, kwargs)


class DetailedAuction(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    queryset = Auction.objects.all()
    serializer_class = GetAuctionRequestSerializer
    lookup_field = 'token'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)



