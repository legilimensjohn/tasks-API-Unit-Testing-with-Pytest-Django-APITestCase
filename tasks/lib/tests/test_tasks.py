"""
Comprehensive Unit Tests for Django Task Management API

Tests cover:
- All CRUD operations (POST, GET, PUT, PATCH, DELETE)
- All possible HTTP status codes (200, 201, 400, 404, 405, etc.)
- JSON response validation
- Edge cases and error handling
- Business logic endpoints
- Service layer testing
"""

import json
from datetime import datetime, timezone
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User

from taskapp.models import Task
from taskapp.serializers import TaskSerializer
from taskapp.services import TaskService


class TaskModelTestCase(TestCase):
    """Test cases for Task model"""
    
    def setUp(self):
        """Set up test data"""
        self.task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'status': 'pending'
        }
    
    def test_task_creation(self):
        """Test task model creation"""
        task = Task.objects.create(**self.task_data)
        
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.priority, 'high')
        self.assertEqual(task.status, 'pending')
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
    
    def test_task_string_representation(self):
        """Test task string representation"""
        task = Task.objects.create(**self.task_data)
        self.assertEqual(str(task), 'Test Task')
    
    def test_task_default_values(self):
        """Test task model default values"""
        minimal_task = Task.objects.create(title='Minimal Task')
        
        self.assertEqual(minimal_task.priority, 'medium')  # Default value
        self.assertEqual(minimal_task.status, 'pending')   # Default value
        self.assertEqual(minimal_task.description, '')     # Default empty


class TaskSerializerTestCase(TestCase):
    """Test cases for Task serializer"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high',
            'status': 'pending'
        }
        
        self.invalid_data = {
            'title': '',  # Empty title should fail
            'priority': 'invalid_priority',
            'status': 'invalid_status'
        }
    
    def test_valid_serializer(self):
        """Test serializer with valid data"""
        serializer = TaskSerializer(data=self.valid_data)
        
        self.assertTrue(serializer.is_valid())
        task = serializer.save()
        self.assertEqual(task.title, 'Test Task')
    
    def test_invalid_serializer_empty_title(self):
        """Test serializer with empty title"""
        data = self.valid_data.copy()
        data['title'] = ''
        
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
    
    def test_invalid_serializer_invalid_priority(self):
        """Test serializer with invalid priority"""
        data = self.valid_data.copy()
        data['priority'] = 'invalid'
        
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('priority', serializer.errors)
    
    def test_serializer_output_fields(self):
        """Test serializer output contains all expected fields"""
        task = Task.objects.create(**self.valid_data)
        serializer = TaskSerializer(task)
        
        expected_fields = {'id', 'title', 'description', 'priority', 'status', 
                          'created_at', 'updated_at', 'due_date'}
        self.assertEqual(set(serializer.data.keys()), expected_fields)


class TaskServiceTestCase(TestCase):
    """Test cases for Task service layer"""
    
    def setUp(self):
        """Set up test data"""
        self.valid_data = {
            'title': 'Service Test Task',
            'description': 'Testing service layer',
            'priority': 'high',
            'status': 'pending'
        }
    
    def test_create_task_service(self):
        """Test task creation through service layer"""
        task = TaskService.create_task(self.valid_data)
        
        self.assertIsInstance(task, Task)
        self.assertEqual(task.title, 'Service Test Task')
        self.assertEqual(Task.objects.count(), 1)
    
    def test_update_task_service(self):
        """Test task update through service layer"""
        task = Task.objects.create(**self.valid_data)
        update_data = {'title': 'Updated Title', 'status': 'completed'}
        
        updated_task = TaskService.update_task(task.id, update_data)
        
        self.assertEqual(updated_task.title, 'Updated Title')
        self.assertEqual(updated_task.status, 'completed')
    
    def test_delete_task_service(self):
        """Test task deletion through service layer"""
        task = Task.objects.create(**self.valid_data)
        task_id = task.id
        
        result = TaskService.delete_task(task_id)
        
        self.assertTrue(result)
        self.assertEqual(Task.objects.count(), 0)
    
    def test_get_high_priority_tasks(self):
        """Test getting high priority tasks"""
        # Create test tasks
        Task.objects.create(title='High Priority 1', priority='high', status='pending')
        Task.objects.create(title='High Priority 2', priority='high', status='in_progress')
        Task.objects.create(title='Low Priority', priority='low', status='pending')
        Task.objects.create(title='Completed High', priority='high', status='completed')
        
        high_priority_tasks = TaskService.get_high_priority_tasks()
        
        self.assertEqual(len(high_priority_tasks), 2)
        for task in high_priority_tasks:
            self.assertEqual(task.priority, 'high')
            self.assertIn(task.status, ['pending', 'in_progress'])


class TaskAPITestCase(APITestCase):
    """Comprehensive API test cases for Task endpoints"""
    
    def setUp(self):
        """Set up test data and client"""
        self.client = APIClient()
        
        # Test data
        self.valid_task_data = {
            'title': 'API Test Task',
            'description': 'Testing API endpoints',
            'priority': 'high',
            'status': 'pending'
        }
        
        self.invalid_task_data = {
            'title': '',  # Empty title
            'priority': 'invalid_priority',
            'status': 'invalid_status'
        }
        
        # Create a test task for update/delete operations
        self.test_task = Task.objects.create(
            title='Existing Task',
            description='Existing Description',
            priority='medium',
            status='pending'
        )
        
        # API URLs
        self.list_url = '/api/tasks/'
        self.detail_url = f'/api/tasks/{self.test_task.id}/'
        self.invalid_detail_url = '/api/tasks/999/'
        
    def test_get_task_list_success(self):
        """Test GET /api/tasks/ - Status 200"""
        response = self.client.get(self.list_url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert response structure
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        
        # Assert task fields
        task_data = response.data[0]
        expected_fields = {'id', 'title', 'description', 'priority', 'status', 
                          'created_at', 'updated_at', 'due_date'}
        self.assertEqual(set(task_data.keys()), expected_fields)
    
    def test_get_task_detail_success(self):
        """Test GET /api/tasks/{id}/ - Status 200"""
        response = self.client.get(self.detail_url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert response data
        self.assertEqual(response.data['id'], self.test_task.id)
        self.assertEqual(response.data['title'], 'Existing Task')
        self.assertEqual(response.data['priority'], 'medium')
    
    def test_get_task_detail_not_found(self):
        """Test GET /api/tasks/{invalid_id}/ - Status 404"""
        response = self.client.get(self.invalid_detail_url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_post_create_task_success(self):
        """Test POST /api/tasks/ - Status 201"""
        response = self.client.post(
            self.list_url, 
            data=json.dumps(self.valid_task_data),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Assert database creation
        self.assertEqual(Task.objects.count(), 2)  # Original + new task
        
        # Assert response data
        self.assertEqual(response.data['title'], 'API Test Task')
        self.assertEqual(response.data['priority'], 'high')
        self.assertIsNotNone(response.data['id'])
        self.assertIsNotNone(response.data['created_at'])
    
    def test_post_create_task_invalid_data(self):
        """Test POST /api/tasks/ with invalid data - Status 400"""
        response = self.client.post(
            self.list_url,
            data=json.dumps(self.invalid_task_data),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Assert validation errors in response
        self.assertIn('errors', response.data)
        
        # Assert no task was created
        self.assertEqual(Task.objects.count(), 1)  # Only original task
    
    def test_put_update_task_success(self):
        """Test PUT /api/tasks/{id}/ - Status 200"""
        update_data = {
            'title': 'Updated Task Title',
            'description': 'Updated Description',
            'priority': 'low',
            'status': 'completed'
        }
        
        response = self.client.put(
            self.detail_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert response data
        self.assertEqual(response.data['title'], 'Updated Task Title')
        self.assertEqual(response.data['status'], 'completed')
        
        # Assert database update
        updated_task = Task.objects.get(id=self.test_task.id)
        self.assertEqual(updated_task.title, 'Updated Task Title')
    
    def test_put_update_task_not_found(self):
        """Test PUT /api/tasks/{invalid_id}/ - Status 404"""
        update_data = {'title': 'Updated Title'}
        
        response = self.client.put(
            self.invalid_detail_url,
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_put_update_task_invalid_data(self):
        """Test PUT /api/tasks/{id}/ with invalid data - Status 400"""
        invalid_update = {
            'title': '',  # Empty title
            'priority': 'invalid_priority'
        }
        
        response = self.client.put(
            self.detail_url,
            data=json.dumps(invalid_update),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_patch_partial_update_success(self):
        """Test PATCH /api/tasks/{id}/ - Status 200"""
        partial_update = {'status': 'in_progress'}
        
        response = self.client.patch(
            self.detail_url,
            data=json.dumps(partial_update),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert only status was updated
        self.assertEqual(response.data['status'], 'in_progress')
        self.assertEqual(response.data['title'], 'Existing Task')  # Unchanged
    
    def test_delete_task_success(self):
        """Test DELETE /api/tasks/{id}/ - Status 204"""
        response = self.client.delete(self.detail_url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Assert task was deleted
        self.assertEqual(Task.objects.count(), 0)
    
    def test_delete_task_not_found(self):
        """Test DELETE /api/tasks/{invalid_id}/ - Status 404"""
        response = self.client.delete(self.invalid_detail_url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_method_not_allowed(self):
        """Test unsupported HTTP methods - Status 405"""
        # Test PATCH on list URL (not supported)
        response = self.client.patch(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test PUT on list URL (not supported)
        response = self.client.put(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TaskBusinessLogicAPITestCase(APITestCase):
    """Test cases for business logic API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test tasks with different priorities and statuses
        Task.objects.create(title='High Priority 1', priority='high', status='pending')
        Task.objects.create(title='High Priority 2', priority='high', status='in_progress')
        Task.objects.create(title='Medium Priority', priority='medium', status='pending')
        Task.objects.create(title='Low Priority', priority='low', status='completed')
        Task.objects.create(title='Completed High', priority='high', status='completed')
    
    def test_get_high_priority_tasks(self):
        """Test GET /api/tasks/high_priority/ - Status 200"""
        url = '/api/tasks/high_priority/'
        response = self.client.get(url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert response data
        self.assertEqual(len(response.data), 2)  # Only pending/in_progress high priority
        
        for task in response.data:
            self.assertEqual(task['priority'], 'high')
            self.assertIn(task['status'], ['pending', 'in_progress'])
    
    def test_get_task_statistics(self):
        """Test GET /api/tasks/statistics/ - Status 200"""
        url = '/api/tasks/statistics/'
        response = self.client.get(url)
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert statistics structure
        expected_fields = {'total', 'pending', 'in_progress', 'completed', 'high_priority'}
        self.assertEqual(set(response.data.keys()), expected_fields)
        
        # Assert statistics values
        self.assertEqual(response.data['total'], 5)
        self.assertEqual(response.data['pending'], 2)
        self.assertEqual(response.data['in_progress'], 1)
        self.assertEqual(response.data['completed'], 2)
        self.assertEqual(response.data['high_priority'], 3)
    
    def test_bulk_update_tasks(self):
        """Test POST /api/tasks/bulk_update/ - Status 200"""
        url = '/api/tasks/bulk_update/'
        
        # Get task IDs for bulk update
        tasks = Task.objects.filter(status='pending')
        task_ids = [task.id for task in tasks]
        
        bulk_data = {
            'task_ids': task_ids,
            'status': 'in_progress'
        }
        
        response = self.client.post(
            url,
            data=json.dumps(bulk_data),
            content_type='application/json'
        )
        
        # Assert status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert response data
        self.assertEqual(response.data['updated_count'], len(task_ids))
        self.assertIn('tasks', response.data)
        
        # Assert database updates
        updated_tasks = Task.objects.filter(id__in=task_ids)
        for task in updated_tasks:
            self.assertEqual(task.status, 'in_progress')


class TaskQueryParameterTestCase(APITestCase):
    """Test cases for query parameter filtering"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create tasks with different statuses and priorities
        Task.objects.create(title='Task 1', priority='high', status='pending')
        Task.objects.create(title='Task 2', priority='medium', status='in_progress')
        Task.objects.create(title='Task 3', priority='low', status='completed')
        Task.objects.create(title='Task 4', priority='high', status='completed')
    
    def test_filter_by_status(self):
        """Test filtering tasks by status"""
        url = '/api/tasks/?status=completed'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        for task in response.data:
            self.assertEqual(task['status'], 'completed')
    
    def test_filter_by_priority(self):
        """Test filtering tasks by priority"""
        url = '/api/tasks/?priority=high'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        for task in response.data:
            self.assertEqual(task['priority'], 'high')
    
    def test_filter_by_multiple_parameters(self):
        """Test filtering by multiple query parameters"""
        url = '/api/tasks/?status=completed&priority=high'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        task = response.data[0]
        self.assertEqual(task['status'], 'completed')
        self.assertEqual(task['priority'], 'high')


class TaskEdgeCaseTestCase(APITestCase):
    """Test cases for edge cases and error scenarios"""
    
    def setUp(self):
        """Set up test client"""
        self.client = APIClient()
    
    def test_malformed_json(self):
        """Test POST with malformed JSON - Status 400"""
        url = '/api/tasks/'
        malformed_json = '{"title": "Test", "priority": high}'  # Missing quotes
        
        response = self.client.post(
            url,
            data=malformed_json,
            content_type='application/json'
        )
        
        # Should handle malformed JSON gracefully
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST])
    
    def test_missing_content_type(self):
        """Test POST without Content-Type header"""
        url = '/api/tasks/'
        data = {'title': 'Test Task'}
        
        response = self.client.post(url, data=data)  # No content_type specified
        
        # Should return HTTP 415 Unsupported Media Type
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
    def test_empty_request_body(self):
        """Test POST with empty request body - Status 400"""
        url = '/api/tasks/'
        
        response = self.client.post(
            url,
            data='',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_very_long_title(self):
        """Test task creation with very long title"""
        url = '/api/tasks/'
        long_title = 'x' * 300  # Assuming max_length=200 in model
        
        data = {
            'title': long_title,
            'priority': 'medium'
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Should fail validation
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)