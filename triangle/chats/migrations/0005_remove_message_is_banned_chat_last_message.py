# Generated by Django 4.0.3 on 2022-08-01 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0004_chatmember_last_checked_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='is_banned',
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chats_in_which_is_last', to='chats.message'),
        ),
    ]