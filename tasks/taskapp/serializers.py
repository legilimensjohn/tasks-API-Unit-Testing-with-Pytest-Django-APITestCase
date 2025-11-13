from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model with comprehensive validation.
    
    Fields:
    - id: Auto-generated unique identifier (read-only)
    - title: Task title (required, max 200 chars)
    - description: Task description (optional)
    - priority: Task priority (required, choices: low, medium, high)
    - status: Task status (required, choices: pending, in_progress, completed)
    - created_at: Creation timestamp (read-only)
    - updated_at: Last update timestamp (read-only)
    - due_date: Optional due date for the task
    """
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'status', 'created_at', 'updated_at', 'due_date']
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'title': {'help_text': 'Task title (required, max 200 characters)'},
            'description': {'help_text': 'Detailed description of the task (optional)'},
            'priority': {'help_text': 'Task priority level: low, medium, or high'},
            'status': {'help_text': 'Current task status: pending, in_progress, or completed'},
            'due_date': {'help_text': 'Optional due date for task completion'},
        }

    def validate_title(self, value):
        """Validate that title is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()

    def validate_priority(self, value):
        """Validate priority choices"""
        valid_priorities = ['low', 'medium', 'high']
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Priority must be one of: {valid_priorities}")
        return value

    def validate_status(self, value):
        """Validate status choices"""
        valid_statuses = ['pending', 'in_progress', 'completed']
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Status must be one of: {valid_statuses}")
        return value
