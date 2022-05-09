import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status

from auction.models import Auction, Tags, Category
from .models import Bid


class BidTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        #create user
        self.user = User.objects.create_user(username='test_user', password='Ab654321')
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(self.user)

        self.user2 = User.objects.create_user(username='test_user2', password='Ab654321')
        self.user2.is_active = True
        self.user2.save()

        #create auction
        category = Category.objects.create(id=1, name="Category")
        tag1 = Tags.objects.create(id=1, name="T1")
        tag2 = Tags.objects.create(id=2, name="T2")
        self.auction = Auction.objects.create(created_at="2019-08-24T14:15:22Z",
                             token="Map5qjBe",
                             name="string",
                             finished_at="2023-08-24T14:15:22Z",
                             mode=1,
                             limit=0,
                             is_private=True,
                             user=self.user,
                             category=category,
                             )
        tags=[tag1, tag2]
        self.auction.tags.set(tags)
        self.auction.save()

    def test_create_bid(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))

        data =  {"price":"60000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["price"], 60000)

        self.auction.finished_at = "2020-08-24T14:15:22Z"
        self.auction.save()
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_get_auction_bids(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))

        Bid.objects.create(user=self.user, auction=self.auction, time="2020-08-24T14:15:22Z", price=1000)
        Bid.objects.create(user=self.user2, auction=self.auction, time="2020-08-24T14:15:30Z", price=2000)

        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)

        filtered_url = url + '?user=1'
        response = self.client.get(filtered_url, format="json")
        self.assertEqual(len(response.data), 1)


    def test_get_user_bids(self):
        url = reverse("bid:get_user_bids")

        Bid.objects.create(user=self.user, auction=self.auction, time="2020-08-24T14:15:22Z", price=1000)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)

        Bid.objects.create(user=self.user, auction=self.auction, time="2020-08-24T14:15:30Z", price=2000)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)

        Bid.objects.create(user=self.user2, auction=self.auction, time="2020-08-24T14:15:30Z", price=3000)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)
