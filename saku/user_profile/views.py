import os
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import Profile


class UpdateProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        email = serializer.data.get("email")
        if email:
            user.email = email
            user.save()
        profile = Profile.objects.filter(user=user)[0]
        old_profile_image = profile.profile_image
        new_profile_image = self.request.data.get("profile_image")
        if new_profile_image and old_profile_image:
            try:
                os.remove(old_profile_image.path)
            except:
                pass
        return profile

    def get_serializer_context(self):
        context = super(UpdateProfile, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context


class DeleteProfilePicture(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        profile = Profile.objects.filter(user=user)[0]
        if profile.profile_image:
            try:
                os.remove(profile.profile_image.path)
            except:
                pass
            profile.profile_image = None
            profile.save()
        return Response(
            {"message": "Profile picture deleted"}, status=status.HTTP_200_OK
        )
