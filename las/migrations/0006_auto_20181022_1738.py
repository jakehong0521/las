# Generated by Django 2.0 on 2018-10-23 00:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('las', '0005_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(default=datetime.date(2018, 10, 22)),
        ),
    ]
