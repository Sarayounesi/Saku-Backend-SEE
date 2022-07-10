import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from auction.models import Auction
from .serializers import CreateCommentSerializer, GetCommentSerializer
from .models import Comment
from user_profile.serializers import GeneralProfileSerializer


class ListCreateComments(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, token):
        auction = get_object_or_404(Auction, token=token)
        request.data["isCollapsed"] = False
        request.data["user"] = request.user.id
        request.data["auction"] = auction.id
        serializer = CreateCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        token = self.kwargs["token"]
        auction = get_object_or_404(Auction, token=token)
        return Comment.objects.filter(auction=auction.id, reply_depth=0)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GetCommentSerializer(
            queryset, many=True, context={"request": self.request, "reply_depth": 0}
        )
        return Response(serializer.data)


class ReplyCommentView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentSerializer

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        reply_depth = comment.reply_depth + 1
        if comment.reply_depth < 2:
            request.data["user"] = request.user.id
            request.data["reply_on"] = comment.id
            request.data["reply_depth"] = reply_depth
            request.data["auction"] = comment.auction.id
            serializer = self.get_serializer(
                data=request.data,
                context={"request": request, "reply_depth": reply_depth},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"massage": "cant reply on this comment"},
            status=status.HTTP_400_BAD_REQUEST,
        )
