from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TaskSerializer
from .models import Task
from .permissions import IsSuperUser,IsTaskOwner, IsAdminUser



class RegisterUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username.strip() or not password.strip():
            return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class LogoutUserAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)



class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsSuperUser | IsAdminUser | IsTaskOwner]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Task.objects.all()  # Superuser sees all tasks
        return Task.objects.filter(user=self.request.user)  # Regular users only see their tasks

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsSuperUser | IsTaskOwner]  # Ensure Hugo is treated correctly
    lookup_field = "pk"

    def get_queryset(self):
        return Task.objects.all()

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_superuser and obj.user != self.request.user:
            self.permission_denied(self.request, message="You do not have permission to access this task.")
        return obj
