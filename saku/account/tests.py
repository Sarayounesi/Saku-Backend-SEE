import json
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from django.contrib.auth.models import User
from user_profile.models import Profile


class AccountTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test_user", password="Ab654321")
        self.user.is_active = True
        self.user.save()

    def test_register_success(self):
        url = reverse("account:register")
        data = {"username": "test_user1", "password": "Ab654321"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_failure_password(self):
        url = reverse("account:register")
        data = {"username": "test_user2", "password": "4321"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_failure_repeatetive_email(self):
        User.objects.create_user(
            username="test_user3", password="Ab654321", email="email@eamil.com"
        )
        url = reverse("account:register")
        data = {
            "username": "test_user2",
            "password": "Ab654321",
            "email": "email@eamil.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            ErrorDetail(
                string="There is another account with this email", code="invalid"
            ),
            response.data["email"],
        )

    def test_register_failure_repeatetive_username(self):
        User.objects.create_user(
            username="test_user3", password="Ab654321", email="email@eamil.com"
        )
        url = reverse("account:register")
        data = {
            "username": "test_user3",
            "password": "Ab654321",
            "email": "email2@eamil.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            ErrorDetail(
                string="A user with that username already exists.", code="unique"
            ),
            response.data["username"],
        )

    def test_login(self):
        url = reverse("account:login")
        response = self.client.post(
            url, {"username": "test_user", "password": "Ab654321"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("refresh" in response.data)
        self.assertTrue("access" in response.data)

    def test_change_password_failure_length(self):
        self.client.force_authenticate(self.user)
        url = reverse("account:change_password")
        data = {
            "old_password": "654321",
            "new_password": "654321",
            "new_password2": "654321",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            ErrorDetail(string="Password was entered incorrectly", code="invalid"),
            response.data["non_field_errors"],
        )

    def test_change_password_failure_length(self):
        self.client.force_authenticate(self.user)
        url = reverse("account:change_password")
        data = {
            "old_password": "Ab654321",
            "new_password": "654321",
            "new_password2": "654321",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_failure_not_match_password(self):
        self.client.force_authenticate(self.user)
        url = reverse("account:change_password")
        data = {
            "old_password": "Ab654321",
            "new_password": "abcd4321",
            "new_password2": "abcd432100",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            ErrorDetail(string="Passwords are not the same", code="invalid"),
            response.data["non_field_errors"],
        )

    def test_change_password_success(self):
        self.client.force_authenticate(self.user)
        url = reverse("account:change_password")
        data = {
            "old_password": "Ab654321",
            "new_password": "abcd4321",
            "new_password2": "abcd4321",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_failure(self):
        url = reverse("account:forgot_password")
        data = {"email": "shahrzad123azari@gmail.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_forgot_password_success(self):
        url = reverse("account:forgot_password")
        data = {"email": "shahrzad123azari@gmail.com"}
        Profile.objects.create(user=self.user, email="shahrzad123azari@gmail.com")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse("account:login")
        response = self.client.post(
            url, {"username": "test_user", "password": "Ab654321"}, format="json"
        )

        url = reverse("account:logout")
        response = self.client.post(
            url, {"refresh": response.data["refresh"]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)