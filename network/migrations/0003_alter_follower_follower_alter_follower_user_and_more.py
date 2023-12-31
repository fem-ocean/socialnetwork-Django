# Generated by Django 4.2.3 on 2023-08-07 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0002_post_like_following_follower"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follower",
            name="follower",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="follower",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followers",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="following",
            name="following",
            field=models.ManyToManyField(
                blank=True,
                default=None,
                null=True,
                related_name="followedby",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="following",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followinguser",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
