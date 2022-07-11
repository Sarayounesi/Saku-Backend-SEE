from rest_framework import serializers


class GeneralCreateResponseSerializer(serializers.Serializer):
    message = serializers.CharField(default="Created!", min_length=5)
    token = serializers.CharField(min_length=8)

    class Meta:
        fields = "__all__"


class GeneralErrorResponseSerializer(serializers.Serializer):
    status_code = serializers.IntegerField(default=400)
    message = serializers.CharField(default="Error!", min_length=5)
    description = serializers.CharField(allow_blank=True)
