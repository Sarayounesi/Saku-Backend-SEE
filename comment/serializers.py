from rest_framework import serializers
from .models import Comment
from user_profile.serializers import GeneralProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = GeneralProfileSerializer(context=self.context)
    replies = CommentSerializer()

    class Meta:
        model: Comment
        fields: ['isCollapsed', 'user', 'date', 'content', 'replies']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.reply_depth != 0:
            self.fields['isCollapsed'].del()
        