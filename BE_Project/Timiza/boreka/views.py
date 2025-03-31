from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TaskSerializer
from .models import Task




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


class LoginUserAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutUserAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)



class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  #Restrict access to logged-in users only

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  #Show only tasks belonging to the logged-in user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  #Ensure the task is saved with the logged-in user


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]  #Restrict access to logged-in users only

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)  #Ensure users only access their own tasks
