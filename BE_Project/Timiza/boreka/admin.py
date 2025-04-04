from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'due_date', 'status']
    search_fields = ['title', 'user__username']
    list_filter = ['status', 'due_date']


admin.site.register(Task, TaskAdmin)

