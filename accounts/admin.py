from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Student, Profile, Comment, Course

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Register your models here.
admin.site.register(Student)

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email", "password"]
    readonly_fields = ["enrolled_courses"]
    inlines = [ProfileInline]

    def enrolled_courses(self, obj):
        return ", ".join([course.title for course in obj.enrolled_courses.all()])

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

admin.site.register(Comment)

admin.site.register(Course)
