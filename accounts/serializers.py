# Going from a Python Object to JSON
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'follows', 'access_token', 'refresh_token' ]