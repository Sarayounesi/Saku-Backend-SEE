from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField
from .models import Comment
from user_profile.serializers import GeneralProfileSerializer


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['isCollapsed', 'id', 'user', 'auction', 'date', 'content', 'replies']
        extra_kwargs = {
            'replies' : {'read_only' : True}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'] = GeneralProfileSerializer(context={'request':self.context.get('request')}, read_only=True)
        reply_depth = self.context.get('reply_depth')
        if reply_depth != None and reply_depth != 0 :
            del self.fields['isCollapsed']
        if reply_depth != None and reply_depth <= 2 :
                self.fields['replies'] = CommentSerializer(many=True, read_only=True, context={'reply_depth':reply_depth+1})
