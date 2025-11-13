#!/usr/bin/env python
"""
Simple test runner to execute our Django tests
"""
import os
import sys
import django

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasks.settings')
django.setup()

# Import test modules after Django setup
from django.test.runner import DiscoverRunner

if __name__ == '__main__':
    print("🧪 Starting Django Test Runner...")
    print("=" * 50)
    
    # Create test runner
    runner = DiscoverRunner(verbosity=2)
    
    # Run specific test module
    test_labels = ['lib.tests.test_tasks']
    
    print(f"Running tests for: {test_labels}")
    print("=" * 50)
    
    # Execute tests
    failures = runner.run_tests(test_labels)
    
    print("=" * 50)
    if failures:
        print(f"❌ {failures} test(s) failed")
        sys.exit(1)
    else:
        print("✅ All tests passed!")
        sys.exit(0)