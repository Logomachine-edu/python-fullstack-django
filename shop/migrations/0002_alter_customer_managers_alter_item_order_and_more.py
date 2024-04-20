# Generated by Django 5.0.1 on 2024-04-15 03:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import shop.service.repo.order


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="customer",
            managers=[
                ("objects", shop.service.repo.order.CustomerManager()),
            ],
        ),
        migrations.AlterField(
            model_name="item",
            name="order",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="shop.order"),
        ),
        migrations.AlterField(
            model_name="itemsphoto",
            name="item_info",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="photo_set",
                related_query_name="photo_set",
                to="shop.iteminfo",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="customer",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
