from chat.models import Chat, Message
from user_profile.models import Profile
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User


class GetChatTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(id=1, username="mehdi")
        self.user2 = User.objects.create(id=2, username="ahmad")
        self.profile = Profile.objects.create(user=self.user, email="google@google.com")
        self.profile = Profile.objects.create(user=self.user2, email="google2@google.com")
        self.client.force_authenticate(self.user)
        self.chat = Chat.objects.create(token='ahmad-mehdi')
        Message.objects.create(chat=self.chat, text="F* you!", sender=self.user)

    def test_get_chat(self):
        response = self.client.get(
            path="/chat/my/"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))

    def test_get_message(self):
        response = self.client.get(
            path="/chat/messages/ahmad/"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.data))
