from django.contrib import admin
from .models import Tags, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Tags)