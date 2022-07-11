import os
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from auction.serializers import (
    CreateAuctionRequestSerializer,
    GetAuctionRequestSerializer,
    UpdateAuctionRequestSerializer,
    GetCategoriesSerializer
)
from rest_framework.response import Response
from saku.serializers import (
    GeneralCreateResponseSerializer,
    GeneralErrorResponseSerializer,
)
from rest_framework.permissions import IsAuthenticated
from auction.models import Auction, Category, Tags
from datetime import datetime


class CreateListAuction(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Auction.objects.order_by("finished_at")

    @swagger_auto_schema(
        responses={
            201: GeneralCreateResponseSerializer,
            400: GeneralErrorResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        tag_names = request.data.get("tags")
        tags = []
        if tag_names:
            try:
                splited_tags = [x.strip() for x in tag_names.split(',')]
            except:
                splited_tags = tags
            for tag in splited_tags:
                tag_instance, _ = Tags.objects.get_or_create(name=tag)
                tags.append(tag_instance)
        request.data["tags"] = tags
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        auctions = Auction.objects.order_by("-created_at")
        if self.request.method == 'GET':
            username = self.request.GET.get('username')
            if username:
                auctions = auctions.filter(user__username=username)

            name = self.request.GET.get('name')
            if name:
                auctions = auctions.filter(name__contains=name)

            mode = self.request.GET.get('mode')
            if mode:
                auctions = auctions.filter(mode=int(mode))

            category = self.request.GET.get('category')
            if category:
                auctions = auctions.filter(category__name=category)

            tag = self.request.GET.get('tag')
            if tag:
                auctions = auctions.filter(tags__in=tag)

            finished = self.request.GET.get('finished')
            if finished and finished == "true":
                auctions = auctions.filter(finished_at__lt=datetime.now())

            elif finished and finished == "false":
                auctions = auctions.filter(finished_at__gte=datetime.now())

            limit = self.request.GET.get('limit')
            if limit:
                auctions = auctions.filter(limit__gte=int(limit))

        return auctions

    @swagger_auto_schema(
        responses={
            201: GeneralCreateResponseSerializer,
            400: GeneralErrorResponseSerializer,
        },
    )
    def get(self, request, *args, **kwargs):
        auctions = self.get_queryset()
        serializer = GetAuctionRequestSerializer(
            auctions, many=True, context={"request": request}
        )
        return Response(serializer.data, status=200)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetAuctionRequestSerializer
        return CreateAuctionRequestSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code != 201:
            return super().finalize_response(request, response, args, kwargs)
        response = GeneralCreateResponseSerializer(
            data={"status_code": 201, "message": "Created!", "token": Auction.objects.get(id=response.data["id"]).token}
        )
        if response.is_valid():
            return super().finalize_response(
                request, Response(response.data, status=201), args, kwargs
            )


class DetailedAuction(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Auction.objects.all()
    lookup_field = "token"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        tag_names = request.data.get("tags")
        tags = []
        if tag_names:
            splited_tags = [x.strip() for x in tag_names.split(',')]
            for tag in splited_tags:
                tag_instance, _ = Tags.objects.get_or_create(name=tag)
                tags.append(tag_instance)
            request.data["tags"] = tags

        instance = self.get_object()
        old_image = instance.auction_image
        new_image = self.request.data.get("auction_image")
        if new_image and old_image:
            try:
                os.remove(old_image.path)
            except:
                pass

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetAuctionRequestSerializer
        return UpdateAuctionRequestSerializer

    def get_serializer_context(self):
        return {"token": self.kwargs["token"]}


class DeleteAuctionPicture(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Auction.objects.all()
    lookup_field = "token"

    def post(self, request, token):
        instance = self.get_object()
        if instance.auction_image:
            try:
                os.remove(instance.auction_image.path)
            except:
                pass
            instance.auction_image = None
            instance.save()
        return Response(
            {"message": "Auction picture deleted"}, status=status.HTTP_200_OK
        )


class CategoryList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetCategoriesSerializer
    queryset = Category.objects.all()
