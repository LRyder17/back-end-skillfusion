# Generated by Django 3.2.20 on 2023-08-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0038_auto_20230807_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(default=''),
        ),
    ]