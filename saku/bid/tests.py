import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from auction.models import Auction, Tags, Category
from .models import Bid


class BidTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        #create user
        self.user = User.objects.create_user(username='test_user', password='Ab654321')
        self.user.is_active = True
        self.user.save()

        self.user2 = User.objects.create_user(username='test_user2', password='Ab654321')
        self.user2.is_active = True
        self.user2.save()

        #create auction
        category = Category.objects.create(name="Category")
        tags = [ Tags.objects.create(name="T1"), Tags.objects.create(name="T2") ]

        self.auction = Auction.objects.create(created_at="2019-08-24T14:15:22Z",
                             token="Map5qjBe",
                             name="string",
                             finished_at="2023-08-24T14:15:22Z",
                             mode=1,
                             limit=400,
                             is_private=False,
                             user=self.user,
                             category=category,
                             )
        self.auction.tags.set(tags)
        self.auction.save()

        self.auction2 = Auction.objects.create(created_at="2019-08-24T14:15:22Z",
                             token="L1sdInBc",
                             name="string",
                             finished_at="2023-08-24T14:15:22Z",
                             mode=2,
                             limit=3000,
                             is_private=True,
                             user=self.user,
                             category=category,
                             )
        self.auction2.tags.set(tags)
        self.auction2.save()

        self.client.force_authenticate(self.user2)


    def test_create_bid_success(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))
        data =  {"price":"60000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["price"], 60000)


    def test_create_bid_failure_auction_owner(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))
        data =  {"price":"60000"}
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='Auction owners cannot bids for their auctions.', code='invalid'),
                      response.data["non_field_errors"])
  

    def test_create_bid_failure_finished_auction(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))
        data =  {"price":"60000"}
        self.auction.finished_at = "2020-08-24T14:15:22Z"
        self.auction.save()
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='Users cannot bid for finished auctions.', code='invalid'),
                      response.data["non_field_errors"])
    

    def test_create_bid_failure_limit_1(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))
        data =  {"price":"300"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='Users cannot bid lower than auction limit.', code='invalid'),
                      response.data["non_field_errors"])

                      
    def test_create_bid_failure_higher_exists(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))

        data =  {"price":"3000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data =  {"price":"2000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='Higher bid for this auction already exists.', code='invalid'),
                      response.data["non_field_errors"])


    def test_create_bid_failure_limit_2(self):
        url = reverse("bid:list_create_bid", args=(self.auction2.token,))
        data =  {"price":"6000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='Users cannot bid higher than auction limit.', code='invalid'),
                      response.data["non_field_errors"])


    def test_create_bid_success_private_auction(self):
        url = reverse("bid:list_create_bid", args=(self.auction2.token,))

        data =  {"price":"2000"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data =  {"price":"2500"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_auction_bids(self):
        url = reverse("bid:list_create_bid", args=(self.auction.token,))

        Bid.objects.create(user=self.user2, auction=self.auction, time="2020-08-24T14:15:22Z", price=1000)
        Bid.objects.create(user=self.user, auction=self.auction, time="2020-08-24T14:15:30Z", price=2000)

        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)

        filtered_url = url + '?user=2'
        response = self.client.get(filtered_url, format="json")
        self.assertEqual(len(response.data), 1)


    def test_get_user_bids(self):
        url = reverse("bid:get_user_bids")

        Bid.objects.create(user=self.user2, auction=self.auction, time="2020-08-24T14:15:22Z", price=1000)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 1)

        Bid.objects.create(user=self.user2, auction=self.auction, time="2020-08-24T14:15:30Z", price=2000)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)

        Bid.objects.create(user=self.user, auction=self.auction, time="2020-08-24T14:15:30Z", price=3000)
        response = self.client.get(url, format="json")
        self.assertEqual(len(response.data), 2)
