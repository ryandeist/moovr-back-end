from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Job
from rest_framework import generics
from .serializers import UserSerializer, JobSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.
class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_user_jobs(self):
        user = self.request.user
        return Job.objects.filter(user=user)
    
    def create_job(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)

class JobDeleteView(generics.DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]
    
    def get_user_jobs(self):
        user = self.request.user
        return Job.objects.filter(user=user)
    
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

