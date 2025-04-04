from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'due_date', 'status']
    search_fields = ['title', 'user__username']
    list_filter = ['status', 'due_date', 'user__username']


    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # If not a superuser, filter to show only their own tasks
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset


admin.site.register(Task, TaskAdmin)

