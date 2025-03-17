from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.JobListView.as_view(), name='job-list'),
    path('jobs/<int:job_id>', views.JobDetailView.as_view(), name='job-detail')
]