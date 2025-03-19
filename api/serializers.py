# Imports
from django.contrib.auth.models import User
from .models import Job, Box
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

# Box Serializer
class BoxSerializer(serializers.ModelSerializer):
    size_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Box
        fields = ['id', 'box_name', 'size', 'size_display', 'box_full', 'created_at', 'job']
        extra_kwargs = {'job': {'read_only': True}}
        
    def get_size_display(self, obj):
        return obj.get_size_display()
    
# Job Serializer
class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'customer_name', 'start_location', 'end_location', 'created_at', 'date', 'user']
        extra_kwargs = {'user': {'read_only': True}}