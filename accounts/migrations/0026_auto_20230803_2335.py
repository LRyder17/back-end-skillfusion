# Generated by Django 3.2.20 on 2023-08-03 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0025_coursesubcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='category',
        ),
        migrations.AddField(
            model_name='course',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.coursesubcategory'),
        ),
    ]