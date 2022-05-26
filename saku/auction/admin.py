from django.contrib import admin
from auction.models import Auction, Tags, Category

# Register your models here.

admin.site.register(Auction)
admin.site.register(Tags)
admin.site.register(Category)
