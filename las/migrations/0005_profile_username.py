# Generated by Django 2.0 on 2018-10-16 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('las', '0004_auto_20181015_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.TextField(blank=True),
        ),
    ]