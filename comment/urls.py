from django.urls import path
from comment.views import ListCreateComments, ReplyCommentView, DeleteCommentView

app_name = 'comment'
urlpatterns = [
    path('<str:token>', ListCreateComments.as_view(), name="list_create_comment"),
    path('reply/<int:pk>', ReplyCommentView.as_view(), name="reply_comment"),
    path('del/<int:pk>', DeleteCommentView.as_view(), name="delete_comment"),
]