# Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, JobSerializer, BoxSerializer
from .models import Job, Box

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
            return Response(serializer.data, status=200)
        except: 
            return Response({'error': 'Unable to get Jobs'}, status=400)

class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=200)
        except Job.DoesNotExist:
            return Response({'error': 'Error getting job.'}, status=400)

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            job.delete()
            return Response({'message': 'Job Deleted Successfully.'}, status=204)
        except:
            return Response({'error': 'Error deleting Job'}, status=400)
        
    def put(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            serializer = JobSerializer(job, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
        except:
            return Response({'error': 'Error updating job'}, status=400)

class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=201)
        except Job.DoesNotExist:
            return Response({'error': 'Job not created'}, status=400)

# Box Views
class BoxListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            boxes = job.boxes.all()
            serializer = BoxSerializer(boxes, many=True)
            return Response(serializer.data, status=200)
        except: 
            return Response({'error': 'Unable to get Boxes'}, status=400)
        
class BoxDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, job_id, box_id):
        try:
            job = Job.objects.get(id=job_id)
            print(job)
            box = job.boxes.get(id=box_id)
            print(box)
            serializer = BoxSerializer(box)
            return Response(serializer.data, status=200)
        except: 
            return Response({'error': 'Unable to get Boxes'}, status=400)
        
class BoxCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            serializer = BoxSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(job=job)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            print("Job not found")
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error during box creation:", str(err))
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)