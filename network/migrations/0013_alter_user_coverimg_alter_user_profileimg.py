# Generated by Django 5.0.1 on 2024-03-19 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0012_alter_user_coverimg_alter_user_profileimg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='coverImg',
            field=models.URLField(blank=True, default='', max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profileImg',
            field=models.URLField(blank=True, default='', max_length=600, null=True),
        ),
    ]
