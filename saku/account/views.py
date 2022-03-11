from django.shortcuts import render
from .serializers import (RegisterSerializer, 
                            ChangePasswordSerializer,
                            ForgotPasswordSerializer)
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from saku.settings import EMAIL_HOST_USER



class Register(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ChangePassword(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def update(self, request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.data.get("new_password"))
            user.save()
            response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPassword(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data['username'])
            new_password = User.objects.make_random_password()
            user.set_password(new_password)
            #delete line below for production
            # user.email = "shahrzad123azari@gmail.com"
            user.save()
            try:
                validate_email(user.email)
            except ValidationError:
                response = {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'There is no valid email for this username.',
                    'data': []
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
            send_mail('New Password', f'Hi {user.username}!\nYour new password is: {new_password}', EMAIL_HOST_USER,
                    recipient_list=[user.email], fail_silently=False)
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'New password was sent to your email.',
                'data': []
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
