# Imports
from django.contrib.auth.models import User
from .models import Job
from rest_framework import serializers

# New User Serializer
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Job Serializer
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'start_location', 'end_location', 'created_at', 'date', 'user']
        extra_kwargs = {'user': {'read_only': True}}