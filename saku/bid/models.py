from django.db import models
from django.contrib.auth.models import User

from auction.models import Auction


class Bid(models.Model):
    time = models.DateTimeField(auto_created=True)
    price = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
