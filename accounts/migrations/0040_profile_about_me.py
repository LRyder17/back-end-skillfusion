# Generated by Django 3.2.20 on 2023-08-07 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_alter_course_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me',
            field=models.TextField(blank=True, null=True),
        ),
    ]
