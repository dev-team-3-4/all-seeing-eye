# Generated by Django 4.0.3 on 2022-06-03 13:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='moderatorinvite',
            unique_together={('smart_contract', 'moderator')},
        ),
    ]