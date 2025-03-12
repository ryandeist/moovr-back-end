from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from . serializer import *
from rest_framework.response import Response

# Create your views here.
class JobsView(APIView):
    serializer_class = JobSerializer
    
    def get(self, request):
        job = [ {"name": job.name, "start_location": job.start_location, "end_location": job.end_location} 
        for job in Job.objects.all()]
        return Response(job)
    
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

