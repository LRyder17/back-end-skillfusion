# Generated by Django 4.2.3 on 2023-07-28 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='access_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='refresh_token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
