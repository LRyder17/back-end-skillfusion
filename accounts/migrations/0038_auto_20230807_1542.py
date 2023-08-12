# Generated by Django 3.2.20 on 2023-08-07 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0037_auto_20230807_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classmeeting',
            name='end_time_meridiem',
            field=models.CharField(choices=[('--', '--'), ('AM', 'AM'), ('PM', 'PM')], default='--', max_length=2),
        ),
        migrations.AlterField(
            model_name='classmeeting',
            name='start_time_meridiem',
            field=models.CharField(choices=[('--', '--'), ('AM', 'AM'), ('PM', 'PM')], default='--', max_length=2),
        ),
    ]