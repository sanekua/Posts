# Generated by Django 3.0.7 on 2020-06-21 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='link',
            field=models.TextField(default='link'),
        ),
    ]
