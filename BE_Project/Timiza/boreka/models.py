from django.contrib.auth.models import User  
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.timezone import now

class Task(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    ]


    PRIORITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
    ]
    

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")  
    due_date = models.DateField(blank=True, null=True)
    priority_level = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")


    def clean(self):
        if self.due_date <= now().date():  
            raise ValidationError("Due date must be a future date.")


    def save(self, *args, **kwargs):
        self.clean()  
        super().save(*args, **kwargs) 
         

    def __str__(self):
        return self.title
