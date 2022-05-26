from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            "user": {"read_only": True}
        }


    def validate_email(self, email):
        user = self.context.get('user')
        if user.email != email and len(Profile.objects.filter(email=email))>0:
            raise serializers.ValidationError("Another user exists with this email address.")
        return email


#TODO: uncomment when profile merged
class GeneralProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    # profile_image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["id", "username", "name"] # , "profile_image"
    
    def get_username(self, obj):
        return obj.username

    def get_name(self, obj):
        profile = Profile.objects.filter(user=obj.id)
        if profile:
            return profile[0].name
        return ""

    # def get_profile_image(self, obj):
    #     profile = Profile.objects.filter(user=obj.id)[0]
    #     return profile.profile_image
