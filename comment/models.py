from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    isCollapsed = models.BooleanField(default=False)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    content = models.CharField(max_Length=200)
    reply_on = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE)
    reply_depth = models.IntegerField(default=0)

    class Meta:
        ordering = ['date']
