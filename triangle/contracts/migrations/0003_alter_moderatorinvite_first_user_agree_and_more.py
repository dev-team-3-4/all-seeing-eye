# Generated by Django 4.0.3 on 2022-06-04 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0002_alter_moderatorinvite_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatorinvite',
            name='first_user_agree',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='moderatorinvite',
            name='second_user_agree',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawalfundsrequest',
            name='first_user_agree',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawalfundsrequest',
            name='moderator_agree',
            field=models.BooleanField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='withdrawalfundsrequest',
            name='second_user_agree',
            field=models.BooleanField(default=None, null=True),
        ),
    ]