# Generated by Django 4.0.3 on 2022-05-27 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='accounts_photos/')),
                ('role', models.SmallIntegerField(default=0)),
                ('ban_until', models.DateTimeField(default=django.utils.timezone.now)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('bank_card_number', models.CharField(blank=True, max_length=16, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PasswordResetObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(default=users.models.generate_key_for_password, max_length=16)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='password_reset_obj', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmailConfirmObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('key', models.CharField(default=users.models.generate_key_for_email, max_length=6)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_confirm_objects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('private_chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='chats.chat')),
                ('user_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_objects', to=settings.AUTH_USER_MODEL)),
                ('user_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_contact_objects', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user_owner', 'user_subject')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='contacts',
            field=models.ManyToManyField(related_name='in_contacts', through='users.Contact', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
