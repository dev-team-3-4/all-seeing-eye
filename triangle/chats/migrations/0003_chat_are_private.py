# Generated by Django 4.0.3 on 2022-05-27 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='are_private',
            field=models.BooleanField(default=False),
        ),
    ]
