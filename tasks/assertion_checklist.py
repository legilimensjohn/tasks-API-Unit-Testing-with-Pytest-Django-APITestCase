"""
COMPLETE ASSERTION CHECKLIST
Ano ang dapat i-assert sa bawat type ng test

Para hindi ka na malito kung ano ang i-assert! 
"""

from rest_framework.test import APITestCase
from rest_framework import status
from taskapp.models import Task
import json

class AssertionChecklist(APITestCase):
    
    # ===========================================
    # 1. GET LIST TESTS (GET /api/tasks/)
    # ===========================================
    def test_get_list_what_to_assert(self):
        """GET List: Ano ang dapat i-assert"""
        
        response = self.client.get('/api/tasks/')
        
        # ✅ ALWAYS ASSERT THESE:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        
        # ✅ IF MAY DATA, ASSERT STRUCTURE:
        if response.data:
            task = response.data[0]
            expected_fields = {'id', 'title', 'description', 'priority', 
                             'status', 'created_at', 'updated_at', 'due_date'}
            self.assertEqual(set(task.keys()), expected_fields)
        
        # ✅ ASSERT COUNT IF EXPECTED:
        # self.assertEqual(len(response.data), expected_count)
    
    # ===========================================
    # 2. GET DETAIL TESTS (GET /api/tasks/{id}/)
    # ===========================================
    def test_get_detail_success_what_to_assert(self):
        """GET Detail Success: Ano ang dapat i-assert"""
        
        # Create test task first
        task = Task.objects.create(title='Test Task', priority='high')
        
        response = self.client.get(f'/api/tasks/{task.id}/')
        
        # ✅ ALWAYS ASSERT:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        
        # ✅ ASSERT SPECIFIC VALUES:
        self.assertEqual(response.data['id'], task.id)
        self.assertEqual(response.data['title'], 'Test Task')
        self.assertEqual(response.data['priority'], 'high')
        
        # ✅ ASSERT ALL REQUIRED FIELDS PRESENT:
        required_fields = ['id', 'title', 'priority', 'status']
        for field in required_fields:
            self.assertIn(field, response.data)
    
    def test_get_detail_not_found_what_to_assert(self):
        """GET Detail 404: Ano ang dapat i-assert"""
        
        response = self.client.get('/api/tasks/99999/')
        
        # ✅ ALWAYS ASSERT:
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # ✅ OPTIONAL: Assert error message format
        # self.assertIn('detail', response.data)
        # self.assertEqual(response.data['detail'], 'Not found.')
    
    # ===========================================
    # 3. POST CREATE TESTS (POST /api/tasks/)
    # ===========================================
    def test_post_create_success_what_to_assert(self):
        """POST Create Success: Ano ang dapat i-assert"""
        
        data = {
            'title': 'New Task',
            'priority': 'medium',
            'status': 'pending'
        }
        
        # Count before creation
        initial_count = Task.objects.count()
        
        response = self.client.post('/api/tasks/', 
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        # ✅ ALWAYS ASSERT:
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsInstance(response.data, dict)
        
        # ✅ ASSERT RETURNED DATA:
        self.assertEqual(response.data['title'], 'New Task')
        self.assertEqual(response.data['priority'], 'medium')
        self.assertIn('id', response.data)  # ID should be generated
        
        # ✅ ASSERT DATABASE CHANGES:
        self.assertEqual(Task.objects.count(), initial_count + 1)
        
        # ✅ ASSERT OBJECT WAS ACTUALLY CREATED:
        created_task = Task.objects.get(id=response.data['id'])
        self.assertEqual(created_task.title, 'New Task')
    
    def test_post_create_validation_error_what_to_assert(self):
        """POST Create Validation Error: Ano ang dapat i-assert"""
        
        invalid_data = {
            'title': '',  # Required field empty
            'priority': 'invalid_choice'
        }
        
        initial_count = Task.objects.count()
        
        response = self.client.post('/api/tasks/',
                                  data=json.dumps(invalid_data),
                                  content_type='application/json')
        
        # ✅ ALWAYS ASSERT:
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # ✅ ASSERT VALIDATION ERRORS:
        # Check your API's error format first!
        if 'errors' in response.data:
            # Your custom format
            self.assertIn('title', response.data['errors'])
        else:
            # Standard DRF format  
            self.assertIn('title', response.data)
        
        # ✅ ASSERT NO DATABASE CHANGES:
        self.assertEqual(Task.objects.count(), initial_count)
    
    # ===========================================
    # 4. PUT UPDATE TESTS (PUT /api/tasks/{id}/)
    # ===========================================
    def test_put_update_success_what_to_assert(self):
        """PUT Update Success: Ano ang dapat i-assert"""
        
        # Create task to update
        task = Task.objects.create(title='Original', priority='low')
        original_id = task.id
        
        update_data = {
            'title': 'Updated Title',
            'priority': 'high',
            'status': 'completed'
        }
        
        response = self.client.put(f'/api/tasks/{task.id}/',
                                 data=json.dumps(update_data),
                                 content_type='application/json')
        
        # ✅ ALWAYS ASSERT:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ✅ ASSERT RETURNED DATA:
        self.assertEqual(response.data['title'], 'Updated Title')
        self.assertEqual(response.data['priority'], 'high')
        self.assertEqual(response.data['id'], original_id)  # ID unchanged
        
        # ✅ ASSERT DATABASE CHANGES:
        task.refresh_from_db()
        self.assertEqual(task.title, 'Updated Title')
        self.assertEqual(task.priority, 'high')
        
        # ✅ ASSERT OBJECT COUNT UNCHANGED:
        # PUT should not create new objects
        # self.assertEqual(Task.objects.count(), 1)
    
    # ===========================================
    # 5. DELETE TESTS (DELETE /api/tasks/{id}/)
    # ===========================================
    def test_delete_success_what_to_assert(self):
        """DELETE Success: Ano ang dapat i-assert"""
        
        task = Task.objects.create(title='To Delete')
        task_id = task.id
        initial_count = Task.objects.count()
        
        response = self.client.delete(f'/api/tasks/{task_id}/')
        
        # ✅ ALWAYS ASSERT:
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # ✅ ASSERT NO RESPONSE BODY (204 has no content):
        # Don't check response.data for 204!
        
        # ✅ ASSERT DATABASE CHANGES:
        self.assertEqual(Task.objects.count(), initial_count - 1)
        
        # ✅ ASSERT OBJECT WAS DELETED:
        self.assertFalse(Task.objects.filter(id=task_id).exists())
    
    # ===========================================
    # 6. VALIDATION TESTING PATTERNS
    # ===========================================
    def test_validation_patterns(self):
        """Common validation testing patterns"""
        
        # Test required fields
        response = self.client.post('/api/tasks/', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test field length limits
        long_title = 'x' * 201  # Over 200 char limit
        response = self.client.post('/api/tasks/', 
                                  data=json.dumps({'title': long_title}),
                                  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test invalid choices
        response = self.client.post('/api/tasks/',
                                  data=json.dumps({
                                      'title': 'Test',
                                      'priority': 'invalid_choice'
                                  }),
                                  content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# ===========================================
# DEBUGGING TIPS - PRINT EVERYTHING!
# ===========================================
"""
DEBUGGING CHECKLIST:

1. Print the URL you're testing:
   print(f"Testing URL: {url}")

2. Print the data you're sending:
   print(f"Sending data: {data}")

3. Print the actual response:
   print(f"Status code: {response.status_code}")
   print(f"Response data: {response.data}")

4. Print what you expected:
   print(f"Expected: {status.HTTP_404_NOT_FOUND}")

5. Check your API's actual behavior in Swagger:
   http://127.0.0.1:8000/swagger/
"""