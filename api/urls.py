# Imports
from django.urls import path
from . import views

# api URL Patterns
urlpatterns = [
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:job_id>/', views.JobDetailView.as_view(), name='job-detail'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job-create'),
    path('jobs/<int:job_id>/boxes/', views.BoxListView.as_view(), name='box-list'),
    path('jobs/<int:job_id>/boxes/<int:box_id>/', views.BoxDetailView.as_view(), name='box-detail'),
    path('jobs/<int:job_id>/boxes/create/', views.BoxCreateView.as_view(), name='box-create'),
    path('jobs/<int:job_id>/boxes/<int:box_id>/items/', views.ItemListView.as_view(), name='item-list'),
]