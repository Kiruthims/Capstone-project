from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task

class TaskPermissionsTestCase(APITestCase):

    def setUp(self):
        """Create users and tasks for testing"""
        # Create users
        self.superuser = User.objects.create_superuser('tester', 'tester@email.com', 'password')
        self.adminuser = User.objects.create_user('adminuser', 'admin@email.com', 'password', is_staff=True)
        self.hugo = User.objects.create_user('hugo', 'hugo@email.com', 'password')

        # Create tasks
        self.task_for_admin = Task.objects.create(title="Admin Task", user=self.adminuser)
        self.task_for_hugo = Task.objects.create(title="Hugo Task", user=self.hugo)

        # Log in the users and store their tokens
        self.superuser_token = self.get_token('tester', 'password')
        self.adminuser_token = self.get_token('adminuser', 'password')
        self.hugo_token = self.get_token('hugo', 'password')

    def get_token(self, username, password):
        """Helper function to get authentication token"""
        response = self.client.post('/api/token/', {'username': username, 'password': password})
        return response.data.get('access')


    def test_superuser_permissions(self):
        """Test that superuser can perform any action on any task"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        
        # Test GET request on any task
        response = self.client.get(f'/api/tasks/{self.task_for_hugo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test PUT request on any task
        response = self.client.put(f'/api/tasks/{self.task_for_hugo.id}/', {'title': 'Updated by Superuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test DELETE request on any task
        response = self.client.delete(f'/api/tasks/{self.task_for_hugo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    
    def test_adminuser_permissions(self):
        """Test that admin user (Njoki) can manage only their own tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.adminuser_token}')
    
        # Test GET request on their task
        response = self.client.get(f'/api/tasks/{self.task_for_admin.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test PUT request on their task
        response = self.client.put(f'/api/tasks/{self.task_for_admin.id}/', {'title': 'Updated by Admin'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test GET request on Hugo's task (should fail)
        response = self.client.get(f'/api/tasks/{self.task_for_hugo.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test PUT request on Hugo's task (should fail)
        response = self.client.put(f'/api/tasks/{self.task_for_hugo.id}/', {'title': 'Updated by Admin'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)



    def test_hugo_permissions(self):
        """Test that Hugo can only GET and POST tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.hugo_token}')
    
        # Test GET request
        response = self.client.get(f'/api/tasks/{self.task_for_hugo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST request 
        response = self.client.post('/api/tasks/', {'title': 'Hugo Task', 'description': 'Testing Hugo'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test PUT request (should fail)
        response = self.client.put(f'/api/tasks/{self.task_for_hugo.id}/', {'title': 'Updated by Hugo'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test DELETE request (should fail)
        response = self.client.delete(f'/api/tasks/{self.task_for_hugo.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)