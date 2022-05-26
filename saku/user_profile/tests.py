import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class ProfileTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test_user', password='Ab654321', email='email@email.com')
        self.user.is_active = True
        self.user.save()
        self.profile = Profile.objects.create(user=self.user, email=self.user.email)
        self.client.force_authenticate(self.user)

    def test_update_profile(self):
        url = reverse("user_profile:update_profile")

        data1 =  {"name" : "Ali", "phone":"09123456789", "email":"email@email.com"} 
        response = self.client.put(url, data1, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data2 =  {"phone" : "090", "email" : "email@email.com"} 
        response = self.client.put(url, data2, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string="Phone number is invalid (.eg '09123456789')", code='invalid'), response.data["phone"])

        data3 =  {"email" : "email.com" } 
        response = self.client.put(url, data3, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='Enter a valid email address.', code='invalid'), response.data["email"])

        data4 =  {} 
        response = self.client.put(url, data4, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
