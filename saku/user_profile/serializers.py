from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            "user": {"read_only": True}
        }

    def validate(self, data):
        email = data.get('email')
        if email:
            if len(Profile.objects.filter(email=email))>0:
                raise serializers.ValidationError("Another user exists with this email address.")
        return data
