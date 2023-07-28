from django.db import models
from django.contrib.auth.models import User

# Create User profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",
                                    related_name="followed_by",
                                    symmetrical=False,
                                    blank=True)
    
    def __str__(self):
        return self.user.username

class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    grade = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'student' 