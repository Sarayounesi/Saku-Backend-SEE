
from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    class Meta:
        db_table = "saku_category"

    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Tags(models.Model):
    class Meta:
        db_table = "saku_Tags"

    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Auction(models.Model):
    class Meta:
        db_table = "saku_auction"

    class Mode(models.IntegerChoices):
        INCREASING = 1
        DECREASING = 2

    name = models.CharField(max_length=20)
    token = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    finished_at = models.DateTimeField()
    mode = models.IntegerField(choices=Mode.choices, default=Mode.INCREASING)
    limit = models.IntegerField(default=0)
    location = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    is_private = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tags)
    participants_num = models.IntegerField(default=0)
    show_best_bid = models.BooleanField(default=False)

    def __str__(self):
        return self.name
