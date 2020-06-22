# Generated by Django 3.0.7 on 2020-06-21 18:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200621_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-10000), django.core.validators.MaxValueValidator(10000)]),
        ),
    ]