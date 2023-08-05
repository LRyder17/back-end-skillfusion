from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.utils import timezone



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
        return ", ".join([enrollment.course.title for enrollment in self.user.enrolled_courses.all()])

    @property
    def teaching_courses(self):
        return ", ".join([course.title for course in self.user.teaching_courses.all()])

    
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

class CourseCategory(models.Model):
    title=models.CharField(max_length=100, null=True, blank=True)
    description=models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural= "Course Categories"

    def __str__(self):
        return self.title

class Course(models.Model):
    LEVEL_CHOICES = [
        ('B', 'Beginner'),
        ('I', 'Intermediate'),
        ('A', 'Advanced'),
    ]

    course_image = models.ImageField(null=True, blank=True, upload_to="images/")
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Allowing null values
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    level_of_difficulty = models.CharField(null=True, blank=True, max_length=1, choices=LEVEL_CHOICES)
    duration_in_weeks = models.PositiveIntegerField(null=True, blank=True, help_text="Enter length of the course in weeks.")
    class_frequency = models.PositiveIntegerField(null=True, blank=True, help_text="Enter how often the class will meet per week.")
    max_students = models.PositiveIntegerField(null=True, blank=True, help_text="Enter maximum number of students. Leave blank for open enrollment.")
    open_enrollment = models.BooleanField(default=True)
    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="teaching_courses",
        null=True, blank=True
    )
    students = models.ManyToManyField(
        User, related_name="enrolled_courses",
        blank=True
    )

    class Meta:
        verbose_name_plural="Courses"

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_courses')
    student=models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_students')
    enrolled_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Enrolled Courses"
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

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

