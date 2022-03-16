import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User


class AccountTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', password='Ab654321')
        self.user.is_active = True
        self.user.save()

    def test_register(self):
        url = reverse("account:register")

        data =  {"username" : "test_user1", "password" : "Ab654321"} 
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data =  {"username" : "test_user2", "password" : "4321"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        url = reverse('account:login')

        response = self.client.post(url, {'username':'test_user', 'password':'Ab654321'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    def test_change_password(self):
        self.client.force_authenticate(self.user)
        url = reverse("account:change_password")
        data =  {"old_password" : "Ab654321", "new_password" : "654321", "new_password2" : "654321" } 
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  
        
        data =  {"old_password" : "Ab654321", "new_password" : "abcd4321", "new_password2" : "abcd432100" } 
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

        data =  {"old_password" : "Ab654321", "new_password" : "abcd4321", "new_password2" : "abcd4321" } 
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  

    def test_forgot_password(self):
        url = reverse("account:forgot_password")
        data =  {"username" : "test_user"} 

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  

        self.user.email = "shahrzad123azari@gmail.com"
        self.user.save()

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)  
