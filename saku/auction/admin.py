from django.contrib import admin
from auction.models import Category, Tags, Auction

# Register your models here.
admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Auction)