# Generated by Django 3.2.9 on 2021-12-03 09:04

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_auto_20211122_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='chat_name',
            field=models.CharField(blank=True, default=chat.models.generate_random_string, max_length=100, null=True, unique=True),
        ),
    ]
