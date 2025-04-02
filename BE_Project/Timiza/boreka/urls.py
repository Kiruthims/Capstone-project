from django.urls import path
from .views import RegisterUserAPIView, LogoutUserAPIView, TaskListCreateView, TaskDetailView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
]
