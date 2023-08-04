# Generated by Django 3.2.20 on 2023-08-03 15:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0020_delete_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='enrolled',
            field=models.ManyToManyField(blank=True, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL),
        ),
    ]