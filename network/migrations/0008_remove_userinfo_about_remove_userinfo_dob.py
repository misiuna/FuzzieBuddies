# Generated by Django 5.0.1 on 2024-03-17 12:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_userinfo_remove_user_userposts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='about',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='dob',
        ),
    ]