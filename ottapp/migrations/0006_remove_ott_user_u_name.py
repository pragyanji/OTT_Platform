# Generated by Django 5.1 on 2024-11-01 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ottapp', '0005_ott_user_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ott_user',
            name='U_name',
        ),
    ]
