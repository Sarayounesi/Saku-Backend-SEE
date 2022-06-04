from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from auction.models import Auction, Tags, Category
from .models import Comment


class CommentTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        #create user
        self.user = User.objects.create_user(username='test_user', password='Ab654321')
        self.user.is_active = True
        self.user.save()
        self.client.force_authenticate(self.user)

        #create auction
        category = Category.objects.create(name="Category")
        tags =[ Tags.objects.create(name="T1"), Tags.objects.create(name="T2") ]
        self.auction = Auction.objects.create(created_at="2019-08-24T14:15:22Z", token="Map5qjBe",
                                            name="string", finished_at="2023-08-24T14:15:22Z", mode=1,
                                            limit=0, is_private=True, user=self.user, category=category,)
        self.auction.tags.set(tags)
        self.auction.save()

        #create comments
        self.comment1 = Comment.objects.create(user=self.user, auction=self.auction,
                                            content="first depth comment", reply_depth=0,
                                            date="2022-08-24T14:15:22Z", reply_on=None)
        self.comment2 = Comment.objects.create(user=self.user, auction=self.auction,
                                            content="second depth comment", reply_depth=1,
                                            date="2022-08-24T14:15:22Z", reply_on=self.comment1)
        self.comment3 = Comment.objects.create(user=self.user, auction=self.auction,
                                            content="third depth comment", reply_depth=2,
                                            date="2022-08-24T14:15:22Z", reply_on=self.comment2)

        self.data =  {"content":"this is a comment"}


    def test_create_comment(self):
        url = reverse("comment:list_create_comment", args=(self.auction.token,))
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["content"], "this is a comment")
    
    def test_create_comment_no_content(self):
        url = reverse("comment:list_create_comment", args=(self.auction.token,))
        data =  {"content":""}
        self.client.force_authenticate(self.user)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reply_comment(self):
        url = reverse("comment:reply_comment", args=(self.comment1.id,))
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reply_comment_depth2(self):
        url = reverse("comment:reply_comment", args=(self.comment3.id,))
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(ErrorDetail(string='cant reply on this comment', code='invalid'),
                      response.data["massage"])

    def test_get_comment(self):
        url = reverse("comment:list_create_comment", args=(self.auction.token,))
        response = self.client.get(url, self.data, format="json")
        comments = Comment.objects.filter(auction=self.auction)
        self.assertEqual(len(response.data), len(comments))
