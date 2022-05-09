from django.contrib.auth.models import User
from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

phone_validator = RegexValidator(regex=r'^09\d{9}$', message="Phone number is invalid (.eg '09123456789')")
national_id_validator = RegexValidator(regex=r'^\d{10}$', message="natinal id is invalid (.eg '1111111111')")


class Profile(models.Model):
    TYPE_CHOICES = (('N', 'natural'), ('L', 'legal'))

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    person_type = models.CharField(choices=TYPE_CHOICES, max_length=1, default='N')
    name = models.CharField(max_length=40, blank=True)
    # national_id = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    national_id = models.CharField(validators=[national_id_validator], max_length=10, blank=True)
    phone = models.CharField(validators=[phone_validator], max_length=11, blank=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    city = models.CharField(max_length=20, blank=True)
    province = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=50, blank=True)
    # picture = 

    def __str__(self):
        return self.name
