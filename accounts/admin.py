from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Student, Profile

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Register your models here.
admin.site.register(Student)

class UserAdmin(admin.ModelAdmin):
    model = User
    # fields = ["username", "first_name", "last_name", "email", "password"]
    fields = ["username"]
    inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)
# admin.site.register(Profile)
