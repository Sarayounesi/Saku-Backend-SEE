import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from auction.models import Auction, Tags, Category
from bid.models import Bid


class HomePageTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        #create users
        self.user1 = User.objects.create_user(username='test_user1', password='Ab654321')
        self.user1.is_active = True
        self.user1.save()
        self.client.force_authenticate(self.user1)

        self.user2 = User.objects.create_user(username='test_user2', password='Ab654321')
        self.user2.is_active = True
        self.user2.save()

        #create auctions
        category = Category.objects.create(name="Category")
        tag1 = Tags.objects.create(name="T1")
        tag2 = Tags.objects.create(name="T2")
        tags=[tag1, tag2]
        self.auction1_user1 = Auction.objects.create(created_at="2019-05-24T14:15:22Z",
                             token="Aap5qjB1",
                             name="string",
                             finished_at="2020-08-24T14:15:22Z",
                             mode=1,
                             limit=0,
                             is_private=True,
                             user=self.user1,
                             category=category,
                             )
        self.auction1_user1.tags.set(tags)
        self.auction1_user1.save()

        self.auction2_user1 = Auction.objects.create(created_at="2020-06-24T14:15:22Z",
                             token="Bap5qjB2",
                             name="string",
                             finished_at="2024-08-24T14:15:22Z",
                             mode=2,
                             limit=1000,
                             is_private=True,
                             user=self.user1,
                             category=category,
                             )
        self.auction2_user1.tags.set(tags)
        self.auction2_user1.save()

        self.auction3_user2 = Auction.objects.create(created_at="2019-07-24T14:15:22Z",
                             token="Cap5qjB3",
                             name="string",
                             finished_at="2024-08-24T14:15:22Z",
                             mode=1,
                             limit=100,
                             is_private=True,
                             user=self.user2,
                             category=category,
                             )
        self.auction3_user2.tags.set(tags)
        self.auction3_user2.save()

        self.auction4_user2 = Auction.objects.create(created_at="2019-08-24T14:15:22Z",
                             token="Dap5qjB4",
                             name="string",
                             finished_at="2024-08-24T14:15:22Z",
                             mode=1,
                             limit=100,
                             is_private=True,
                             user=self.user2,
                             category=category,
                             )
        self.auction4_user2.tags.set(tags)
        self.auction4_user2.save()

        #create bids
        self.bid1_user2 = Bid.objects.create(user=self.user2, price=500, auction=self.auction1_user1, time="2020-07-24T14:15:22Z")
        self.auction1_user1.participants_num = 1
        self.auction1_user1.best_bid = self.bid1_user2
        self.auction1_user1.save()

        self.bid2_user2 = Bid.objects.create(user=self.user2, price=400, auction=self.auction2_user1, time="2020-07-24T14:15:22Z")
        self.auction2_user1.participants_num = 1
        self.auction2_user1.save()

        self.bid3_user1 = Bid.objects.create(user=self.user1, price=300, auction=self.auction3_user2, time="2020-07-24T14:15:22Z")
        self.auction3_user2.participants_num = 1
        self.auction3_user2.best_bid = self.bid3_user1
        self.auction3_user2.save()

        self.bid4_user1 = Bid.objects.create(user=self.user1, price=200, auction=self.auction4_user2, time="2020-07-24T14:15:22Z")
        self.auction4_user2.participants_num = 1
        self.auction4_user2.save()


    def test_homepage(self):
        url = reverse("homepage:homepage", args=(2020,))
        response = self.client.get(url, format="json")
        data = response.data["data"]

        income = data['income']
        seccussfull_auction_count = data['seccussfull_auction_count']
        auctions_participants_num = data['auctions_participants_num']
        auctions_count = data['auctions_count']
        last_auctions_participated = data['last_auctions_participated']
        last_auctions_created = data['last_auctions_created']
        income_list = data['income_list']
        your_colaberation_list = data['your_colaberation_list']
        your_colaberation_count = data['your_colaberation_count']
        others_colaberation_list = data['others_colaberation_list']
        others_colaberation_count = data['others_colaberation_count']
        expense_list = data['expense_list']
        expense = data['expense']
        auction1_participate_count = data['auction1_participate_count']
        auction1_create_count = data['auction1_create_count']
        auction2_participate_count = data['auction2_participate_count']
        auction2_create_count = data['auction2_create_count']
        yearly_income_list = data['yearly_income_list']
        yearly_expense_list = data['yearly_expense_list']

        #income
        self.assertEqual(income, 500)
        self.assertEqual(len(income_list), 1)
        self.assertEqual(income_list[0], 500)
        self.assertEqual(sum(income_list), income)
        #colaberation
        self.assertEqual(sum(your_colaberation_list), your_colaberation_count)
        self.assertEqual(sum(others_colaberation_list), others_colaberation_count)
        #expense
        self.assertEqual(expense, 300)
        self.assertEqual(len(expense_list), 1)
        self.assertEqual(expense_list[0], 300)
        self.assertEqual(sum(expense_list), expense)
        #auction created
        self.assertEqual(auctions_count, 2)
        self.assertEqual(len(last_auctions_created), 2)
        self.assertEqual(auction1_create_count, 1)
        self.assertEqual(auction2_create_count, 1)
        self.assertEqual(auction1_create_count + auction2_create_count, auctions_count)
        #auction participated
        self.assertEqual(seccussfull_auction_count, 1)
        self.assertEqual(auctions_participants_num,2)
        self.assertEqual(len(last_auctions_participated), 2)
        self.assertEqual(auction1_participate_count, 2)
        self.assertEqual(auction2_participate_count, 0)
        self.assertEqual(auction1_participate_count + auction2_participate_count, auctions_participants_num)
        #yearly report
        self.assertEqual(len(yearly_income_list), 1)
        self.assertEqual(yearly_income_list[0], 500)
        self.assertEqual(len(yearly_expense_list), 0)
