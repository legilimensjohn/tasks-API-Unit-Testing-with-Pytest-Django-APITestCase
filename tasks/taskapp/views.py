from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Task
from .serializers import TaskSerializer
from .services import TaskService

@api_view(['POST'])
def simple_create_task(request):
    """Simple task creation with detailed error messages"""
    try:
        # Use service layer for business logic
        task = TaskService.create_task(request.data)
        
        return Response({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'created_at': task.created_at,
            'updated_at': task.updated_at,
            'due_date': task.due_date,
            'message': 'Task created successfully!'
        }, status=201)
        
    except Exception as e:
        return Response({
            'error': str(e),
            'received_data': request.data,
            'message': 'Task creation failed'
        }, status=400)

class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on Task model.
    
    Provides these endpoints:
    - GET /api/tasks/ - List all tasks
    - POST /api/tasks/ - Create a new task
    - GET /api/tasks/{id}/ - Retrieve a specific task
    - PUT /api/tasks/{id}/ - Update a specific task (full)
    - PATCH /api/tasks/{id}/ - Partially update a specific task
    - DELETE /api/tasks/{id}/ - Delete a specific task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    @swagger_auto_schema(
        operation_summary="List all tasks",
        operation_description="Retrieve a list of all tasks. Supports filtering by status and priority.",
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by task status (pending, in_progress, completed)", type=openapi.TYPE_STRING),
            openapi.Parameter('priority', openapi.IN_QUERY, description="Filter by task priority (low, medium, high)", type=openapi.TYPE_STRING),
        ],
        responses={
            200: TaskSerializer(many=True),
            400: "Bad Request - Invalid parameters"
        },
        tags=['Tasks']
    )
    def list(self, request, *args, **kwargs):
        """GET /api/tasks/ - List all tasks with optional filtering"""
        queryset = self.get_queryset()
        
        # Apply filters if provided
        status_filter = request.GET.get('status')
        priority_filter = request.GET.get('priority')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Create a new task",
        operation_description="Create a new task with the provided data. Title, priority, and status are required fields.",
        request_body=TaskSerializer,
        responses={
            201: TaskSerializer,
            400: "Bad Request - Validation errors"
        },
        tags=['Tasks']
    )
    def create(self, request, *args, **kwargs):
        """POST /api/tasks/ - Create a new task"""
        print(f"Received data: {request.data}")  # Debug print
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(f"Validation errors: {serializer.errors}")  # Debug print
        return Response({
            'errors': serializer.errors,
            'received_data': request.data,
            'message': 'Validation failed'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        """GET /api/tasks/{id}/ - Get a specific task"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """PUT /api/tasks/{id}/ - Update a specific task (full update)"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, *args, **kwargs):
        """PATCH /api/tasks/{id}/ - Partially update a specific task"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        """DELETE /api/tasks/{id}/ - Delete a specific task"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Task deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
    def get_queryset(self):
        """
        Optionally filter tasks by status or priority
        Example: /api/tasks/?status=pending&priority=high
        """
        queryset = Task.objects.all()
        status_filter = self.request.query_params.get('status')
        priority_filter = self.request.query_params.get('priority')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
            
        return queryset.order_by('-created_at')

    @swagger_auto_schema(
        operation_summary="Get high priority tasks",
        operation_description="Retrieve all tasks with 'high' priority status.",
        responses={
            200: TaskSerializer(many=True)
        },
        tags=['Business Logic']
    )
    @action(detail=False, methods=['get'])
    def high_priority(self, request):
        """GET /api/tasks/high_priority/ - Get all high priority tasks"""
        high_priority_tasks = TaskService.get_high_priority_tasks()
        serializer = self.get_serializer(high_priority_tasks, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Get task statistics",
        operation_description="Retrieve comprehensive statistics about all tasks including counts by status and priority.",
        responses={
            200: openapi.Response(
                description="Task statistics",
                examples={
                    "application/json": {
                        "total_tasks": 15,
                        "pending": 5,
                        "in_progress": 7,
                        "completed": 3,
                        "high_priority": 4,
                        "medium_priority": 8,
                        "low_priority": 3
                    }
                }
            )
        },
        tags=['Business Logic']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """GET /api/tasks/statistics/ - Get task statistics"""
        stats = TaskService.get_task_statistics()
        return Response(stats)
    
    @swagger_auto_schema(
        operation_summary="Bulk update tasks",
        operation_description="Update multiple tasks at once. Provide an array of task IDs and the fields to update.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='Array of task IDs to update'
                ),
                'status': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['pending', 'in_progress', 'completed'],
                    description='New status for the tasks'
                ),
                'priority': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['low', 'medium', 'high'],
                    description='New priority for the tasks'
                ),
            },
            required=['task_ids'],
            example={
                "task_ids": [1, 2, 3],
                "status": "completed"
            }
        ),
        responses={
            200: openapi.Response(
                description="Bulk update successful",
                examples={
                    "application/json": {
                        "updated_count": 3,
                        "tasks": "Array of updated task objects"
                    }
                }
            ),
            400: "Bad Request - Invalid data"
        },
        tags=['Business Logic']
    )
    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """POST /api/tasks/bulk_update/ - Bulk update tasks"""
        task_ids = request.data.get('task_ids', [])
        
        # Extract update data (excluding task_ids)
        update_data = {k: v for k, v in request.data.items() if k != 'task_ids'}
        
        try:
            updated_tasks = TaskService.bulk_update_tasks(task_ids, update_data)
            serializer = self.get_serializer(updated_tasks, many=True)
            return Response({
                'updated_count': len(updated_tasks),
                'tasks': serializer.data
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

def api_info(request):
    """API information endpoint"""
    return JsonResponse({
        'message': 'Task Management API',
        'version': '1.0',
        'endpoints': {
            'GET /api/tasks/': 'List all tasks',
            'POST /api/tasks/': 'Create a new task',
            'GET /api/tasks/{id}/': 'Get specific task',
            'PUT /api/tasks/{id}/': 'Update specific task (full)',
            'PATCH /api/tasks/{id}/': 'Partially update specific task',
            'DELETE /api/tasks/{id}/': 'Delete specific task'
        },
        'filters': {
            'status': 'pending, in_progress, completed',
            'priority': 'low, medium, high'
        }
    })
