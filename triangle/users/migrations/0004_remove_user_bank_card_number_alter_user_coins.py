# Generated by Django 4.0.3 on 2022-09-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_coins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bank_card_number',
        ),
        migrations.AlterField(
            model_name='user',
            name='coins',
            field=models.BigIntegerField(default=0),
        ),
    ]
