# Generated by Django 3.1.3 on 2020-12-26 15:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_auto_20201223_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 28, 15, 40, 1, 388555, tzinfo=utc)),
        ),
    ]
