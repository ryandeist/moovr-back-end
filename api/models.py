# Imports
from django.db import models
from django.contrib.auth.models import User

SIZES = (
    ('1', 'Small'),
    ('2', 'Medium'),
    ('3', 'Large'),
    ('4', 'Extra Large')
)

# Models

class Job(models.Model):
    customer_name = models.CharField(max_length=100)
    start_location = models.CharField(max_length=100)
    end_location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    
    def __str__(self):
        return self.customer_name

class Box(models.Model):
    box_name = models.CharField(max_length=100)
    box_description = models.TextField(max_length=250)
    size = models.CharField(
        max_length=1,
        choices=SIZES,
        default=SIZES[0][0]
        )
    box_full = models.BooleanField(default=False)
    is_heavy = models.BooleanField(default=False)
    is_fragile = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    job = models.ForeignKey(Job, related_name='boxes', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.box_name

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    is_fragile = models.BooleanField(default=False)
    is_heavy = models.BooleanField(default=False)
    
    box = models.ForeignKey(Box, related_name='items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name