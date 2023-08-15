from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Comment, Course, Enrollment, CourseCategory, GroupStudyMeeting, StudyRequestAcceptance

# Mix Profile info into User info
class ProfileInline(admin.StackedInline):
    model = Profile

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "first_name", "last_name", "email", "password", "is_teacher_display", "enrolled_courses"]
    readonly_fields = ["enrolled_courses", "is_teacher_display"]
    inlines = [ProfileInline]

    def is_teacher_display(self, obj):
        return obj.profile.is_teacher
    is_teacher_display.short_description = 'Is Teacher'

    def enrolled_courses(self, obj):
        enrollments = Enrollment.objects.filter(student=obj)
        return ", ".join([enrollment.course.title for enrollment in enrollments])
    enrolled_courses.short_description = 'Enrolled Courses'


admin.site.unregister(User)

admin.site.register(User, UserAdmin)

admin.site.register(Comment)

# admin.site.register(Course)
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'category', 'teacher',)
    search_fields = ('title', 'subject', 'category', 'teacher',)
admin.site.register(CourseCategory)
admin.site.register(Enrollment)

admin.site.register(GroupStudyMeeting)

admin.site.register(StudyRequestAcceptance)