"""
Debug Testing Guide: How to Fix Status Code Issues

Common Problem: Expected 404/400 but getting 200/201
"""

from rest_framework.test import APITestCase
from rest_framework import status
import json

class DebugTestExample(APITestCase):
    
    def test_debug_404_issue(self):
        """Example: How to debug 404 issues"""
        
        # 1. ALWAYS print what you're testing
        url = '/api/tasks/999/'  # Non-existent ID
        print(f"Testing URL: {url}")
        
        response = self.client.get(url)
        
        # 2. ALWAYS print actual response
        print(f"Actual Status Code: {response.status_code}")
        print(f"Expected Status Code: {status.HTTP_404_NOT_FOUND}")
        print(f"Response Data: {response.data}")
        print(f"Response Content: {response.content}")
        
        # 3. Check if URL pattern exists
        # If you get 404 when expecting 200, URL might be wrong
        # If you get 200 when expecting 404, the resource might exist
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_debug_400_issue(self):
        """Example: How to debug 400 validation issues"""
        
        # Invalid data that should trigger 400
        invalid_data = {
            'title': '',  # Empty title should be invalid
            'priority': 'invalid_priority'  # Invalid choice
        }
        
        print(f"Sending Data: {invalid_data}")
        
        response = self.client.post('/api/tasks/', data=json.dumps(invalid_data), 
                                  content_type='application/json')
        
        print(f"Actual Status: {response.status_code}")
        print(f"Response Data: {response.data}")
        
        # If you get 201 instead of 400, your validation might not be working
        # Check if serializer validation is properly implemented
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Also assert the validation errors
        self.assertIn('title', response.data.get('errors', {}))