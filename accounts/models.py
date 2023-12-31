from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User, AbstractUser
from django.dispatch import receiver
from django.utils import timezone


class CourseCategory(models.Model):
    title=models.CharField(max_length=100, null=True, blank=True)
    description=models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural= "Course Categories"

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about_me = models.TextField(null=True, blank=True)
    interested_categories = models.ManyToManyField(CourseCategory, blank=True)
    is_teacher = models.BooleanField(default=False)
    follows = models.ManyToManyField("self",
                                    related_name="followed_by",
                                    symmetrical=False,
                                    blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    instagram_link = models.CharField(null=True, blank=True, max_length=100)

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


class Course(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]

    teacher = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="teaching_courses",
        null=True, blank=True
    )
    students = models.ManyToManyField(
        User, related_name="enrolled_courses",
        blank=True
    )
    likes = models.ManyToManyField(
        User, related_name="liked_courses",
        blank=True
    )
    
    favorites = models.ManyToManyField(
        User, related_name="favorited_courses",
        blank=True
    )

    course_image = models.ImageField(null=True, blank=True, upload_to="images/")
    start_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, 
                                                null=True, 
                                                blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    description = models.TextField(default="")
    level_of_difficulty = models.CharField(null=True, blank=True, 
                                           max_length=13, choices=LEVEL_CHOICES)
    duration_in_weeks = models.PositiveIntegerField(
                                                    null=True, blank=True, 
                                                    help_text="Enter length of the course in weeks.")
    class_frequency = models.PositiveIntegerField(
                                                null=True, blank=True, 
                                                help_text="Enter how often the class will meet per week.")
    max_students = models.PositiveIntegerField(
                                            null=True, blank=True, 
                                            help_text="Enter maximum number of students. Leave blank for open enrollment.")
    open_enrollment = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural="Courses"
    
    def check_max_students(self):
        if self.max_students is not None:
            student_count = self.enrolled_courses.count()
            if student_count >= self.max_students:
                self.open_enrollment = False
                self.save()
    
    def has_study_request(self):
        return GroupStudyMeeting.objects.filter(course=self).exists()

    def number_of_likes(self):
        return self.likes.count()
    
    def number_of_favorites(self):
        return self.favorites.count()

    def check_max_students(self):
        if self.max_students is not None:
            student_count = self.enrolled_courses.count()
            if student_count >= self.max_students:
                self.open_enrollment = False
                self.save()
    
    def has_study_request(self):
        return GroupStudyMeeting.objects.filter(course=self).exists()

    def __str__(self):
        return self.title if self.title else 'No Title'


# **************************** Class Meeting Modles *****************
    
class GroupStudyMeeting(models.Model):
    MEETING_TYPES = [
        ('ONLINE', 'Online'),
        ('IN_PERSON', 'In-person'),
        ('HYBRID', 'Hybrid'),
    ]
    MERIDIEM_CHOICES = [
    ('AM', 'AM'),
    ('PM', 'PM'),
    ]
    course = models.ForeignKey(Course, related_name='class_meeting_schedule', 
                                        on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    meeting_type = models.CharField(max_length=10, choices=MEETING_TYPES, default='ONLINE')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_time_meridiem = models.CharField(max_length=2, choices=MERIDIEM_CHOICES)
    end_time_meridiem = models.CharField(max_length=2, choices=MERIDIEM_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def accepted_users_names(self):
        accepted_users = StudyRequestAcceptance.objects.filter(study_request=self, 
                                                               accepted=True)
        return ", ".join([acceptance.user.username for acceptance in accepted_users])

    @property
    def is_accepted(self):
        return StudyRequestAcceptance.objects.filter(study_request=self, 
                                                     accepted=True).exists()

    @property
    def accepted_count(self):
        return 1 + StudyRequestAcceptance.objects.filter(
                                            study_request=self, 
                                            accepted=True).exclude(
                                            user=self.created_by).count()
    
    class Meta:
        verbose_name = "Group Meeting"
        verbose_name_plural = "Group Meetings"
    
    def __str__(self):
        return f"{self.course.title} - {self.date} - {self.start_time}"
    
class StudyRequestAcceptance(models.Model):
    study_request = models.ForeignKey(GroupStudyMeeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, 
                               related_name='study_request_acceptances', 
                               null=True) 
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural="Study Request Acceptances"
        unique_together = ('study_request', 'user')
    
    def __str__(self):
        return f"{self.user.username} accepted study request for {self.study_request.course.title}"

    def save(self, *args, **kwargs):
        if not self.course:
            self.course = self.study_request.course
        super(StudyRequestAcceptance, self).save(*args, **kwargs)


class Enrollment(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, 
                             related_name='enrolled_courses')
    student=models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='enrolled_students')
    enrolled_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural="Enrolled Courses"
    
    def save(self, *args, **kwargs):
        super(Enrollment, self).save(*args, **kwargs)
        self.course.check_max_students()
    
    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="comments",
        on_delete=models.SET_NULL,
        null=True,
        )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, 
        related_name="course_comments", 
        null=True)

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

