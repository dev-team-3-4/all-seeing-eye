# Generated by Django 4.0.3 on 2022-09-15 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0005_remove_message_is_banned_chat_last_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmember',
            name='last_checked_message',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chats.message'),
        ),
    ]