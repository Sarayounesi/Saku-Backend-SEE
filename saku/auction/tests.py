from django.test import Client
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from auction.models import Auction, Tags, Category


# Create your tests here.
class CreateAuctionTest(APITestCase):

    def setUp(self) -> None:
        self.client = Client()
        User.objects.create(id=1, username="Mehdi")
        Category.objects.create(id=1, name="Category")
        Tags.objects.create(id=1, name="T1")
        Tags.objects.create(id=2, name="T2")
        self.request_data = {"created_at": "2019-08-24T14:15:22Z",
                             "name": "string",
                             "finished_at": "2019-08-24T14:15:22Z",
                             "mode": 1,
                             "limit": 0,
                             "is_private": True,
                             "user": 0,
                             "category": "C1",
                             "tags": ["T1", "T2"]}

    def test_not_found_user(self):
        response = self.client.post(path='/auction/', data=self.request_data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertIn(ErrorDetail(string='Invalid pk "0" - object does not exist.', code='does_not_exist'),
                      response.data["user"])

    def test_with_equal_dates(self):
        self.request_data["user"] = 1
        response = self.client.post(path='/auction/', data=self.request_data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertIn(ErrorDetail(string="created_at can't be greater or equal to finished_at", code='invalid'),
                      response.data["non_field_errors"])

    def test_create_valid_auction(self):
        auctions_count = Auction.objects.count()
        self.request_data["user"] = 1
        self.request_data["finished_at"] = "2020-08-24T14:15:22Z"
        response = self.client.post(path='/auction/', data=self.request_data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(auctions_count + 1, Auction.objects.count())
