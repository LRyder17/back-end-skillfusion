# Generated by Django 3.2.20 on 2023-08-12 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0042_auto_20230808_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_comments', to='accounts.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='groupstudymeeting',
            name='end_time_meridiem',
            field=models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], max_length=2),
        ),
        migrations.AlterField(
            model_name='groupstudymeeting',
            name='start_time_meridiem',
            field=models.CharField(choices=[('AM', 'AM'), ('PM', 'PM')], max_length=2),
        ),
    ]