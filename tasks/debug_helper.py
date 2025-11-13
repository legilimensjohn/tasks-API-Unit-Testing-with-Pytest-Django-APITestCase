"""
QUICK DEBUG HELPER - Add this to any failing test

Copy-paste this function to debug any test na hindi mo makuha yung expected result
"""

def debug_response(self, response, expected_status, test_name=""):
    """
    Debug helper function - add this to your test class
    """
    print(f"\n{'='*50}")
    print(f"DEBUG: {test_name}")
    print(f"{'='*50}")
    print(f"Expected Status: {expected_status}")
    print(f"Actual Status: {response.status_code}")
    print(f"Response Data: {response.data}")
    print(f"Response Content: {response.content}")
    
    if hasattr(response, 'wsgi_request'):
        print(f"Request URL: {response.wsgi_request.get_full_path()}")
        print(f"Request Method: {response.wsgi_request.method}")
    
    print(f"{'='*50}\n")
    
    # Assert with debug info
    assert response.status_code == expected_status, \
        f"Expected {expected_status}, got {response.status_code}. Data: {response.data}"

# EXAMPLE USAGE:
class MyTestCase(APITestCase):
    
    def test_something_failing(self):
        """Example na laging nag-fail"""
        
        response = self.client.get('/api/tasks/999/')
        
        # Add this line to debug:
        self.debug_response(response, status.HTTP_404_NOT_FOUND, "Test Get Non-Existent Task")
        
        # Your original assertion
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)