
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class ListCreateComments(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, token):
        auction = get_object_or_404(Auction, token=token)
        request.data['user'] = request.user.id
        request.data['auction'] = auction.id
        request.data['date'] = datetime.datetime.now()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        token = self.kwargs['token']
        auction = get_object_or_404(Auction, token=token)
        return Comment.objects.filter(auction=auction)

    def get_serializer_context(self):
        context={'request' : self.request}
        return context


class ReplyCommentView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        if(comment.reply_depth < 2):
            request.data['user'] = request.user.id
            request.data['date'] = datetime.datetime.now()
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            reply = serializer.save()
            reply.reply_on = comment
            reply.reply_depth = comment.reply_depth + 1
            reply.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'massage':'cant reply on this comment'}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_context(self):
        context={'request' : self.request}
        return context   


class DeleteCommentView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def get_object(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)

        #HERE: change reply_depth?
        # if comment.reply_depth != 0:
        #     parent_comment = comment.reply_on
        #     if parent_comment:

        return comment