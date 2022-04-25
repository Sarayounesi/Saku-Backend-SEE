from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import Profile


class UpdateProfile(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        profile = Profile.objects.filter(user = self.request.user)
        if len(profile) != 0:
            queryset = profile[0]
        else:
            queryset = Profile.objects.create(user=self.request.user, national_id='0', email='')
        return queryset
