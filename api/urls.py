# Imports
from django.urls import path
from . import views

# api URL Patterns
urlpatterns = [
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:pk>/boxes/', views.BoxListView.as_view(), name='box-list'),
]