from rest_framework import serializers
from django.contrib.auth.models import User
from user_profile.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
        }

    def validate_email(self, email):
        if User.objects.filter(email=email):
            raise serializers.ValidationError(
                "There is another account with this email"
            )
        return email

    def create(self, validated_data):
        # create user account
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        # create user profile
        Profile.objects.create(user=user, national_id="0", email=user.email)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    new_password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "new_password2"]

    def validate_old_password(self, data):
        user = self.context["request"].user
        if not user.check_password(data):
            raise serializers.ValidationError(("Password was entered incorrectly"))
        return data

    def validate(self, data):
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError("Passwords are not the same")
        return data


class ForgotPasswordSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        # fields = ['username']
        fields = ["email"]
