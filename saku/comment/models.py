from django.db import models
from django.contrib.auth.models import User
from auction.models import Auction


class Comment(models.Model):
    isCollapsed = models.BooleanField(default=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=200)
    reply_on = models.ForeignKey(
        "self", related_name="replies", on_delete=models.CASCADE, null=True
    )
    reply_depth = models.IntegerField(default=0)

    class Meta:
        ordering = ["date"]
