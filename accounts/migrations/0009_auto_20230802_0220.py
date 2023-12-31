# Generated by Django 3.2.20 on 2023-08-02 02:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comment_like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subject', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('level_of_difficulty', models.CharField(choices=[('B', 'Beginner'), ('I', 'Intermediate'), ('A', 'Advanced')], max_length=1)),
                ('duration_in_weeks', models.PositiveIntegerField(help_text='Enter length of the course in weeks.')),
                ('class_frequency', models.PositiveIntegerField(help_text='Enter how often the class will meet per week.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('enrolled_students_count', models.PositiveIntegerField(default=0)),
                ('course_image', models.ImageField(blank=True, null=True, upload_to='course_images/')),
                ('class_date', models.DateField(blank=True, null=True)),
                ('class_time', models.TimeField(blank=True, null=True)),
                ('students', models.ManyToManyField(blank=True, related_name='enrolled_courses', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teaching_courses', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'course',
            },
        ),
    ]
