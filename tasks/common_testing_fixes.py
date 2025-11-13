"""
Common Testing Issues and Solutions - Tagalog/English Guide

ISSUE 1: Expected 404 but getting 200
Problem: Ang URL na ginagamit mo ay existing pala
Solution: Check mo yung URL at ID na ginagamit mo

ISSUE 2: Expected 400 but getting 201/200  
Problem: Ang validation hindi nag-trigger
Solution: Check mo yung serializer validation

ISSUE 3: Expected 200 but getting 404
Problem: Wrong URL pattern or missing trailing slash
Solution: Check mo yung URL configuration
"""

from rest_framework.test import APITestCase
from rest_framework import status
from taskapp.models import Task
import json

class CommonTestingFixes(APITestCase):
    
    def setUp(self):
        # Create test data
        self.existing_task = Task.objects.create(
            title='Existing Task',
            priority='high', 
            status='pending'
        )
    
    def test_fix_404_issue(self):
        """FIX: Para sa 404 testing"""
        
        # ✅ CORRECT: Use non-existent ID
        non_existent_url = '/api/tasks/99999/'  # ID na sure na wala
        response = self.client.get(non_existent_url)
        
        print(f"URL: {non_existent_url}")
        print(f"Status: {response.status_code}")
        
        # This should be 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # ❌ WRONG: Using existing ID
        # existing_url = f'/api/tasks/{self.existing_task.id}/'
        # This will return 200, not 404!
    
    def test_fix_400_validation_issue(self):
        """FIX: Para sa 400 validation testing"""
        
        # ✅ CORRECT: Send truly invalid data
        invalid_data = {
            # Missing required field 'title'
            'priority': 'invalid_choice',  # Invalid choice
            'status': 'invalid_status'     # Invalid choice
        }
        
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(invalid_data),
            content_type='application/json'  # IMPORTANT!
        )
        
        print(f"Data sent: {invalid_data}")
        print(f"Status: {response.status_code}")
        print(f"Errors: {response.data}")
        
        # This should be 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Assert specific validation errors
        if 'errors' in response.data:
            # Your API returns errors in 'errors' key
            self.assertIn('title', response.data['errors'])
        else:
            # Standard DRF format
            self.assertIn('title', response.data)
    
    def test_fix_trailing_slash_issue(self):
        """FIX: Para sa trailing slash issues"""
        
        # ✅ CORRECT: With trailing slash
        correct_url = '/api/tasks/'
        response = self.client.get(correct_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ❌ COMMON MISTAKE: Missing trailing slash
        # wrong_url = '/api/tasks'  # Missing /
        # This might return 301 or 404
    
    def test_fix_content_type_issue(self):
        """FIX: Para sa Content-Type issues"""
        
        data = {'title': 'Test Task', 'priority': 'high'}
        
        # ✅ CORRECT: With proper Content-Type
        response = self.client.post(
            '/api/tasks/',
            data=json.dumps(data),
            content_type='application/json'  # REQUIRED!
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # ❌ WRONG: Missing Content-Type
        # response = self.client.post('/api/tasks/', data=data)
        # This might return 415 Unsupported Media Type