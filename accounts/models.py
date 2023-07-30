from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                    related_name="followed_by",
                                    symmetrical=False,
                                    blank=True)
    date_modified = models.DateTimeField(User, auto_now=True)
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    
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