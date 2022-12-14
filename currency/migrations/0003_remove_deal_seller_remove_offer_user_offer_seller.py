# Generated by Django 4.1.3 on 2022-11-27 15:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("currency", "0002_alter_deal_buyer_alter_deal_seller"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="deal",
            name="seller",
        ),
        migrations.RemoveField(
            model_name="offer",
            name="user",
        ),
        migrations.AddField(
            model_name="offer",
            name="seller",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offers",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Seller",
            ),
            preserve_default=False,
        ),
    ]
