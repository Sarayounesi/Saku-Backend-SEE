import base64
from drf_yasg.utils import swagger_auto_schema
from auction.serializers import CreateAuctionRequestSerializer, GetAuctionRequestSerializer, GetCategoriesSerializer
from rest_framework import generics, status
from auction.serializers import CreateAuctionRequestSerializer, GetAuctionRequestSerializer, UpdateAuctionRequestSerializer
from rest_framework.response import Response
from saku.serializers import GeneralCreateResponseSerializer, GeneralErrorResponseSerializer
from rest_framework.permissions import IsAuthenticated
from auction.models import Auction, Category, Tags


class CreateListAuction(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Auction.objects.order_by('finished_at')

    @swagger_auto_schema(
        responses={201: GeneralCreateResponseSerializer,
                   400: GeneralErrorResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        tag_names = request.data.get('tags')
        tags = []
        if tag_names:
            for tag in tag_names:
                tag_instance, _ = Tags.objects.get_or_create(name=tag)
                tags.append(tag_instance)
        request.data['tags'] = tags
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={201: GeneralCreateResponseSerializer,
                   400: GeneralErrorResponseSerializer},
    )
    def get(self, request, *args, **kwargs):
        auctions = self.get_queryset()
        serializer = GetAuctionRequestSerializer(auctions, many=True, context={'request' : request})
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


class DetailedAuction(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Auction.objects.all()
    lookup_field = 'token'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request,*args, **kwargs):
        tag_names = request.data.get('tags')
        tags = []
        if tag_names:
            for tag in tag_names:
                tag_instance, _ = Tags.objects.get_or_create(name=tag)
                tags.append(tag_instance)
            request.data['tags'] = tags

        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetAuctionRequestSerializer
        return UpdateAuctionRequestSerializer

    def get_serializer_context(self):
        return {"token": self.kwargs['token']}


class CategoryList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetCategoriesSerializer
    queryset = Category.objects.all()
