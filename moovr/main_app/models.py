from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("job_detail", kwargs={"pk": self.pk})
    