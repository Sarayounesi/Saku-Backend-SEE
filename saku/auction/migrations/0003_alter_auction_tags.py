# Generated by Django 4.0.3 on 2022-05-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auction", "0002_auction_description_auction_location_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auction",
            name="tags",
            field=models.ManyToManyField(blank=True, to="auction.tags"),
        ),
    ]
