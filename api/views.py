# Imports
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, JobSerializer, BoxSerializer, ItemSerializer
from .models import Job, Box, Item

# Authorization Views
class SignupView(APIView):
    def post(self, request):
        if request.data["password"] != request.data["passwordConfirm"]:
            return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
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
            else:
                print("validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print("Error during account creation:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        try:
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
                }, status=status.HTTP_200_OK)
            else:
                print("Invalid Credentials")
                return Response({"error": "Invalid Credentials."}, status=status.HTTP_404_NOT_FOUND)
        except:
            print("Invalid Credentials")
            return Response({"error": "Invalid Credentials."}, status=status.HTTP_400_BAD_REQUEST)

# Job Model Views
class JobListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            jobs = Job.objects.filter(user=user)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as err: 
            print("Error Fetching Jobs:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class JobDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            print("Job not found")
            return Response({"error": "Job Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error fetching Job:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            job.delete()
            return Response({"message": "Job Deleted Successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Job.DoesNotExist:
            print("Job not found")
            return Response({"error": "Job Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error deleting Job:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id, user=request.user)
            serializer = JobSerializer(job, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Job.DoesNotExist:
            print("Job not found")
            return Response({"error": "Job Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error updating Job:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class JobCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = JobSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else: 
                print("validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            print("Error during job creation:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

# Box Views
class BoxListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            boxes = job.boxes.all()
            serializer = BoxSerializer(boxes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            print("Job not found")
            return Response({"error": "Job Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err: 
            print("Error Fetching Boxes:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

class BoxDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id, box_id):
        try:
            job = Job.objects.get(id=job_id)
            box = job.boxes.get(id=box_id)
            serializer = BoxSerializer(box)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            print("Job not found")
            return Response({"error": "Job Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err: 
            print("Error Fetching Box:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, job_id, box_id):
        try:
            box = Box.objects.get(id=box_id)
            box.delete()
            return Response({"message": "Box deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Box.DoesNotExist:
            print("Box not found")
            return Response({"error": "Box Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error Deleting Box:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_id, box_id):
        try:
            job = Job.objects.get(id=job_id)
            box = Box.objects.get(id=box_id, job=job)
            serializer = BoxSerializer(box, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Box.DoesNotExist:
            print("Box not found.")
            return Response({"error": "Box Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error updating Box", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

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
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            print("Error during box creation:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)

# Item Views
class ItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, job_id, box_id):
        try:
            box = Box.objects.get(id=box_id)
            items = box.items.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Box.DoesNotExist:
            print("Box not found")
            return Response({"error": "Box Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err: 
            print("Error Fetching Items:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        
class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, job_id, box_id, item_id):
        print (request)
        print(job_id, box_id, item_id)
        try:
            box = Box.objects.get(id=box_id)
            item = box.items.get(id=item_id)
            serializer = ItemSerializer(item)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Box.DoesNotExist:
            print("Box not found")
            return Response({"error": "Box Not Found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err: 
            print("Error Fetching Items:", str(err))
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
