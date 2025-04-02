from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TaskSerializer
from .models import Task
from.permissions import IsAdminUser, IsTaskOwner



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


# List and Create Tasks
class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  #Restrict access to logged-in users only

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  #Automatically assign user to task they have created

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

# Retrieve, Update, Delete Tasks
class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwner]  #Restrict access to logged-in users only and also ensure that only owners of tasks can modify

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  #Ensure users only access their own tasks

    