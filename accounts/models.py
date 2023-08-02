from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)
    follows = models.ManyToManyField("self",
                                    related_name="followed_by",
                                    symmetrical=False,
                                    blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)

    @property
    def enrolled_courses(self):
        return self.user.enrolled_courses.all()

    @property
    def teaching_courses(self):
        return self.user.teaching_courses.all()
    
    def __str__(self):
        return self.user.username
    
# Create Profile when new User signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # have the User follow themselves
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'student' 


class Course(models.Model):
    LEVEL_CHOICES = [
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    level_of_difficulty = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    duration_in_weeks = models.PositiveIntegerField(help_text="Enter length of the course in weeks.")
    class_frequency = models.PositiveIntegerField(help_text="Enter how often the class will meet per week.")
    max_students = models.PositiveIntegerField(null=True, blank=True, help_text="Enter maximum number of students. Leave blank for open enrollment.")
    open_enrollment = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(
        User, related_name="teaching_courses",
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    students = models.ManyToManyField(
        User, related_name="enrolled_courses",
        blank=True
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)], null=True, blank=True)
    enrolled_students_count = models.PositiveIntegerField(default=0)
    course_image = models.ImageField(upload_to='images/', null=True, blank=True)
    class_date = models.DateField(null=True, blank=True)
    class_time = models.TimeField(null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        db_table = 'course'

    def save(self, *args, **kwargs):
        if self.max_students and self.enrolled_students_count >= self.max_students:
            self.open_enrollment = False
        super().save(*args, **kwargs)

    
# class ClassMeetings(models.Model):
#     MEETING_TYPES = [
#         ('ONLINE', 'Online'),
#         ('IN_PERSON', 'In-person'),
#         ('HYBRID', 'Hybrid'),
#     ]
#     course = models.ForeignKey(Course, related_name='class_meetings', on_delete=models.CASCADE)
#     meeting_type = models.CharField(max_length=10, choices=MEETING_TYPES, default='ONLINE')
#     date = models.DateField()
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     location = models.CharField(max_length=255, blank=True, null=True)
#     meeting_link = models.URLField(blank=True, null=True)
#     description = models.TextField(blank=True, null=True)

#     class Meta:
#         verbose_name = "Class Meeting"
#         verbose_name_plural = "Class Meetings"
    
#     def __str__(self):
#         return f"{self.course.course_subject} - {self.date} - {self.start_time} to {self.end_time}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comments",
        on_delete=models.DO_NOTHING
        )
    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="comment_like", blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at: %Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )