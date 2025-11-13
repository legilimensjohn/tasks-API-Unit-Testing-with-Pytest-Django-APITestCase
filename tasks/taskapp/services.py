"""
Business Logic Layer - Services for Task operations
Separates business logic from views and serializers
"""
from django.db import transaction
from django.db import models
from django.core.exceptions import ValidationError
from .models import Task
from .serializers import TaskSerializer
from typing import Dict, List, Optional


class TaskService:
    """Service layer for Task business logic"""
    
    @staticmethod
    def create_task(data: Dict) -> Task:
        """Create a new task with business logic"""
        serializer = TaskSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.save()
    
    @staticmethod
    def update_task(task_id: int, data: Dict) -> Task:
        """Update task with business logic"""
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise ValidationError(f"Task with id {task_id} not found")
        
        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            return serializer.save()
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Delete task with business logic"""
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return True
        except Task.DoesNotExist:
            raise ValidationError(f"Task with id {task_id} not found")
    
    @staticmethod
    def get_tasks_by_status(status: str) -> List[Task]:
        """Get tasks filtered by status"""
        return Task.objects.filter(status=status).order_by('-created_at')
    
    @staticmethod
    def get_high_priority_tasks() -> List[Task]:
        """Business logic: Get high priority pending tasks"""
        return Task.objects.filter(
            priority='high', 
            status__in=['pending', 'in_progress']
        ).order_by('-created_at')
    
    @staticmethod
    @transaction.atomic
    def bulk_update_status(task_ids: List[int], new_status: str) -> int:
        """Business logic: Bulk update task status"""
        updated_count = Task.objects.filter(
            id__in=task_ids
        ).update(status=new_status)
        return updated_count
    
    @staticmethod
    def get_task_statistics() -> Dict:
        """Business logic: Get task statistics"""
        from django.db.models import Count
        
        stats = Task.objects.aggregate(
            total=Count('id'),
            pending=Count('id', filter=models.Q(status='pending')),
            in_progress=Count('id', filter=models.Q(status='in_progress')), 
            completed=Count('id', filter=models.Q(status='completed')),
            high_priority=Count('id', filter=models.Q(priority='high'))
        )
        return stats
    
    @staticmethod
    @transaction.atomic
    def bulk_update_tasks(task_ids: List[int], update_data: Dict) -> List[Task]:
        """Business logic: Bulk update multiple tasks"""
        tasks = Task.objects.filter(id__in=task_ids)
        updated_tasks = []
        
        for task in tasks:
            serializer = TaskSerializer(task, data=update_data, partial=True)
            if serializer.is_valid(raise_exception=True):
                updated_task = serializer.save()
                updated_tasks.append(updated_task)
        
        return updated_tasks
