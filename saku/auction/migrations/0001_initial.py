# Generated by Django 4.0.3 on 2022-04-29 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "name",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
            ],
            options={
                "db_table": "saku_category",
            },
        ),
        migrations.CreateModel(
            name="Tags",
            fields=[
                (
                    "name",
                    models.CharField(max_length=20, primary_key=True, serialize=False),
                ),
            ],
            options={
                "db_table": "saku_Tags",
            },
        ),
        migrations.CreateModel(
            name="Auction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_created=True)),
                ("name", models.CharField(max_length=20)),
                ("token", models.CharField(max_length=8, unique=True)),
                ("finished_at", models.DateTimeField()),
                (
                    "mode",
                    models.IntegerField(
                        choices=[(1, "Increasing"), (2, "Decreasing")], default=1
                    ),
                ),
                ("limit", models.IntegerField(default=0)),
                ("is_private", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="auction.category",
                    ),
                ),
                ("tags", models.ManyToManyField(to="auction.tags")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "saku_auction",
            },
        ),
    ]
