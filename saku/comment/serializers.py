from rest_framework import serializers
from .models import Comment
from user_profile.serializers import GeneralProfileSerializer


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['reply_depth', 'reply_on']
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
                self.fields['replies'] = GetCommentSerializer(many=True, read_only=True, context={'reply_depth':reply_depth+1})


class CreateCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        instance = Comment.objects.create(**validated_data)
        return instance
