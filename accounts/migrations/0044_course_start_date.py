# Generated by Django 3.2.20 on 2023-08-12 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0043_auto_20230812_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]