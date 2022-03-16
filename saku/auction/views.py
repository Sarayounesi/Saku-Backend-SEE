from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from auction.serializers import CreateAuctionRequestSerializer
from rest_framework.response import Response
from saku.serializers import GeneralCreateResponseSerializer, GeneralErrorResponseSerializer
from rest_framework.permissions import AllowAny


class CreateAuction(generics.CreateAPIView):
    permission_classes = (AllowAny,)  # TODO: change to IsAuthorized after auth has merged.
    serializer_class = CreateAuctionRequestSerializer

    @swagger_auto_schema(
        responses={201: GeneralCreateResponseSerializer,
                   400: GeneralErrorResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code != 201:
            return super().finalize_response(request, response, args, kwargs)

        response = GeneralCreateResponseSerializer(data={'status_code': 201, 'message': 'Created!'})
        if response.is_valid():
            return super().finalize_response(request, Response(response.data, status=201), args, kwargs)
