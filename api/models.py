# Imports
from django.db import models
from django.contrib.auth.models import User

# Models
class Job(models.Model):
    name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    
    def __str__(self):
        return self.name