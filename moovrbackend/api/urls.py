from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.JobListCreateView.as_view(), name='note_list'),
    path('jobs/delete/<int:pk>/', views.JobDeleteView.as_view(), name='note_delete'),
]