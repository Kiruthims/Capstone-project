from django.contrib.auth.models import User
from django.db import models



class Task(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name ="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(blank = True, null = True)
    is_completed = models.BooleanField(default = False)
    due_date = models.DateField(blank = True, null = True)

    def __str__(self):
        return self.title
