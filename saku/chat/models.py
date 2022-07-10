from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Chat(models.Model):
    token = models.CharField(
        max_length=25, blank=False, editable=False, null=False, default=""
    )
    created_at = models.DateTimeField(auto_now=True)

    def contact_username(self, username):
        return str(self.token).split("-").pop(username)[0]


class Message(models.Model):
    text = models.CharField(null=False, max_length=120)
    created_at = models.DateTimeField(auto_now=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
