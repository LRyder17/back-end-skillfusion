# Generated by Django 3.2.20 on 2023-08-02 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_profile_is_teacher'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student',
        ),
    ]
