# Going from a Python Object to JSON
from rest_framework import serializers
from .models import Profile, Comment, Course, GroupStudyMeeting, Enrollment

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    enrolled_courses = serializers.StringRelatedField(read_only=True)
    teaching_courses = serializers.StringRelatedField(read_only=True)
    follows = serializers.StringRelatedField(many=True, read_only=True)
    followed_by = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user', 'about_me', 'is_teacher', 'follows', 'followed_by',
            'date_modified', 'profile_image', 'access_token', 'refresh_token',
            'enrolled_courses', 'teaching_courses'
        )
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user', 'body', 'created_at', 'likes_count']

    def get_likes_count(self, obj):
        return obj.number_of_likes()

class CourseSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    teacher = serializers.StringRelatedField(read_only=True)
    students = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            'course_image', 'category', 'creator', 'created_at', 'updated_at', 
            'title', 'subject', 'description', 'level_of_difficulty', 
            'duration_in_weeks', 'class_frequency', 'max_students', 
            'open_enrollment', 'teacher', 'students'
        )
    
class GroupStudyMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupStudyMeeting
        fields = (
            'course', 'meeting_type', 'date', 'start_time',
            'end_time', 'start_time_meridiem', 'end_time_meridiem',
            'location', 'meeting_link', 'description',
        )
    
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ('course', 'student', 'enrolled_time',)