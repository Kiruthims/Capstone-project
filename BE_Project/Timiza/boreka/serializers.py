from rest_framework import serializers
from .models import Task
from django.utils import timezone



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  
        extra_kwargs = {'user': {'read_only': True}}


    def validate_due_date(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date must be in the future.")
        return value
