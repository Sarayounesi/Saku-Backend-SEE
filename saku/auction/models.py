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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_created=True)
    finished_at = models.DateTimeField()
    mode = models.IntegerField(choices=Mode.choices, default=Mode.INCREASING)
    limit = models.IntegerField(default=0)
    is_private = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return self.name
