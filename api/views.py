# Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, JobSerializer
from .models import Job

# Authorization Views
class SignupView(APIView):
    def post(self, request):
        if request.data['password'] != request.data['passwordConfirm']:
            return Response({"error": "Passwords do not match."}, status=400)
            
        serializer =SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                "message": "User created successfully.", 
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                }
            }, status=status.HTTP_201_CREATED)
            
        return Response({"error": "Sign Up Failed."}, status=400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                }
            })
        return Response({"error": "Invalid Credentials."}, status=400)

# Job Model Views
class JobListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            jobs = Job.objects.filter(user=user)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        except: 
            return Response({'error': 'Unable to Get Jobs'}, status=400)

class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            job = Job.objects.get(pk=pk, user=request.user)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=200)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)

    def delete(self, request, pk):
        try:
            job = Job.objects.get(pk=pk, user=request.user)
            job.delete()
            return Response({'message': 'Job Deleted Successfully.'}, status=204)
        except Job.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)

class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=201)
        except Job.DoesNotExist:
            return Response({'error': 'Job not created'}, status=404)