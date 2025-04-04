from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class TaskPermissionsTestCase(APITestCase):
    
    def setUp(self):
        """Create users and tasks for testing"""
        self.superuser = User.objects.create_superuser('tester', 'tester@email.com', 'Hugo')
        self.adminuser = User.objects.create_user('adminuser', 'admin@email.com', 'adminpass123', is_staff=True)
        self.hugo = User.objects.create_user('hugo', 'hugo@email.com', 'hugopass123')

        # Log in the users and store their tokens
        self.superuser_token = self.get_token('tester', 'Hugo')
        self.adminuser_token = self.get_token('adminuser', 'adminpass123')
        self.hugo_token = self.get_token('hugo', 'hugopass123')

    def get_token(self, username, password):
        """Helper function to get authentication token"""
        response = self.client.post('/api/token/', {'username': username, 'password': password})
        return response.data.get('access')

    def tearDown(self):
        """Cleanup actions after each test"""
        self.client.credentials()  # Reset authentication

    def test_hugo_permissions(self):
        """Test that Hugo can only GET and POST tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.hugo_token}')
        
        # Test GET request
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST request 
        response = self.client.post('/api/tasks/', {'title': 'Hugo Task', 'description': 'Testing Hugo'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test PUT request 
        task_id = response.data['id']
        response = self.client.put(f'/api/tasks/{task_id}/', {'title': 'Updated Title', 'description': 'Updated Desc'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test DELETE request 
        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_adminuser_permissions(self):
        """Test that AdminUser can manage their own tasks"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.adminuser_token}')
        
        # Create task
        response = self.client.post('/api/tasks/', {'title': 'Admin Task', 'description': 'Testing Admin'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task_id = response.data['id']

        # Admin should be able to update their own tasks
        response = self.client.put(f'/api/tasks/{task_id}/', {'title': 'Updated Admin Task', 'description': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin should be able to delete their own tasks
        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_superuser_permissions(self):
        """Test that Superuser can do anything"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.superuser_token}')
        
        # Test GET (view all tasks)
        response = self.client.get('/api/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test creating a task
        response = self.client.post('/api/tasks/', {'title': 'Superuser Task', 'description': 'Testing Superuser'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task_id = response.data['id']

        # Superuser should be able to update any task
        response = self.client.put(f'/api/tasks/{task_id}/', {'title': 'Updated Superuser Task', 'description': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Superuser should be able to delete any task
        response = self.client.delete(f'/api/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
