# Django Task Management API

A comprehensive RESTful API built with Django REST Framework featuring clean architecture, proper separation of concerns, comprehensive CRUD operations, and **interactive Swagger documentation** for task management.

## 📚 **API Documentation**

### **Interactive Documentation**

- **🔗 Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/) - Interactive API explorer
- **🔗 ReDoc**: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) - Clean documentation
- **🔗 OpenAPI Schema**: [http://127.0.0.1:8000/swagger.json](http://127.0.0.1:8000/swagger.json) - Raw schema

### **Documentation Features**

- ✅ Interactive "Try it out" functionality
- ✅ Complete endpoint documentation with examples
- ✅ Request/response schema validation
- ✅ Error response documentation
- ✅ Parameter descriptions and constraints
- ✅ Business logic endpoint documentation

## 🏗️ Architecture Overview

This project follows **Clean Architecture** principles with proper separation of concerns:

```
📁 taskapp/
├── models.py      → Data Layer (Database schema)
├── serializers.py → Validation Layer (Input/Output validation)
├── services.py    → Business Logic Layer (Core business rules)
├── views.py       → Presentation Layer (API endpoints)
├── urls.py        → Routing Layer (URL configuration)
└── admin.py       → Admin interface
```

## 🎯 Design Patterns & Principles

### 1. **Separation of Concerns**

Each layer has a single responsibility:

- **Models**: Define data structure and database relationships
- **Serializers**: Handle data validation and transformation
- **Services**: Contain business logic and complex operations
- **Views**: Process HTTP requests and return responses
- **URLs**: Route requests to appropriate views

### 2. **Service Layer Pattern**

Business logic is separated from views into dedicated service classes:

```python
class TaskService:
    @staticmethod
    def create_task(data: Dict) -> Task:
        """Business logic for task creation"""

    @staticmethod
    def get_high_priority_tasks() -> List[Task]:
        """Business rule: Get high priority pending tasks"""
```

### 3. **Repository Pattern** (via Django ORM)

Data access is abstracted through Django's ORM, providing a clean interface to the database.

## 🚀 Features

### Core CRUD Operations

- ✅ **Create** tasks with validation
- ✅ **Read** tasks (single & multiple)
- ✅ **Update** tasks (full & partial)
- ✅ **Delete** tasks

### Advanced Features

- 📊 **Task Statistics** - Get comprehensive task analytics
- 🔥 **High Priority Filter** - Retrieve urgent tasks
- 📦 **Bulk Operations** - Update multiple tasks at once
- 🔍 **Query Filtering** - Filter by status, priority, etc.
- ✨ **Data Validation** - Comprehensive input validation

## 📡 API Endpoints

### Standard CRUD

```http
GET    /api/tasks/           # List all tasks
POST   /api/tasks/           # Create new task
GET    /api/tasks/{id}/      # Get specific task
PUT    /api/tasks/{id}/      # Update task (full)
PATCH  /api/tasks/{id}/      # Update task (partial)
DELETE /api/tasks/{id}/      # Delete task
```

### Business Logic Endpoints

```http
GET    /api/tasks/high_priority/    # Get high priority tasks
GET    /api/tasks/statistics/       # Get task statistics
POST   /api/tasks/bulk_update/      # Bulk update task status
```

### Query Parameters

```http
GET /api/tasks/?status=pending&priority=high
GET /api/tasks/?status=completed
```

## 🗄️ Data Model

```python
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(choices=['low', 'medium', 'high'])
    status = models.CharField(choices=['pending', 'in_progress', 'completed'])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
```

## 📝 Request/Response Examples

### Create Task

```json
POST /api/tasks/
{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "priority": "high",
    "status": "pending",
    "due_date": "2025-09-30T17:00:00Z"
}
```

### Response

```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive README and API docs",
  "priority": "high",
  "status": "pending",
  "created_at": "2025-09-29T10:00:00Z",
  "updated_at": "2025-09-29T10:00:00Z",
  "due_date": "2025-09-30T17:00:00Z"
}
```

### Task Statistics

```json
GET /api/tasks/statistics/
{
    "total": 15,
    "pending": 5,
    "in_progress": 3,
    "completed": 7,
    "high_priority": 4
}
```

## ⚙️ Installation & Setup

### Prerequisites

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+

### Installation

```bash
# Clone repository
git clone https://github.com/legilimensjohn/tasks.git
cd tasks

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install django djangorestframework

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## 🧪 Testing

### Using Postman

Import the API collection or manually test endpoints:

- Set `Content-Type: application/json` header
- Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Include trailing slashes in URLs

### Using Django Browsable API

Navigate to `http://127.0.0.1:8000/api/tasks/` in your browser to use the interactive API interface.

### Using cURL

```bash
# Create a task
curl -X POST http://127.0.0.1:8000/api/tasks/ \\
  -H "Content-Type: application/json" \\
  -d '{"title": "Test Task", "priority": "medium"}'

# Get all tasks
curl http://127.0.0.1:8000/api/tasks/

# Update a task
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \\
  -H "Content-Type: application/json" \\
  -d '{"status": "completed"}'
```

## 🔧 Configuration

### Settings

Key configuration in `settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Django REST Framework
    'taskapp',         # Your app
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}
```

## 📚 Code Examples

### Service Layer Usage

```python
# In views.py
from .services import TaskService

def create_task_view(request):
    task = TaskService.create_task(request.data)
    return Response(TaskSerializer(task).data)
```

### Custom Validation

```python
# In serializers.py
def validate_title(self, value):
    if not value or not value.strip():
        raise serializers.ValidationError("Title cannot be empty")
    return value.strip()
```

### Business Logic

```python
# In services.py
@staticmethod
def get_high_priority_tasks() -> List[Task]:
    return Task.objects.filter(
        priority='high',
        status__in=['pending', 'in_progress']
    ).order_by('-created_at')
```

## 🏆 Best Practices Implemented

- ✅ **RESTful API Design** - Proper HTTP methods and status codes
- ✅ **Clean Architecture** - Separation of concerns across layers
- ✅ **Input Validation** - Comprehensive data validation
- ✅ **Error Handling** - Proper error responses and status codes
- ✅ **Documentation** - Self-documenting code and API
- ✅ **Scalability** - Service layer for complex business logic
- ✅ **Security** - Built-in Django security features

## 📊 Status Codes

| Code | Meaning            | When                       |
| ---- | ------------------ | -------------------------- |
| 200  | OK                 | Successful GET, PUT, PATCH |
| 201  | Created            | Successful POST            |
| 204  | No Content         | Successful DELETE          |
| 400  | Bad Request        | Validation errors          |
| 404  | Not Found          | Resource doesn't exist     |
| 405  | Method Not Allowed | Wrong HTTP method          |

## 🚀 **Quick Start with Swagger**

### **1. Install Dependencies**

```bash
pip install django djangorestframework drf-yasg
```

### **2. Run Migrations**

```bash
python manage.py migrate
```

### **3. Start the Server**

```bash
python manage.py runserver
```

### **4. Access Documentation**

Open your browser and visit:

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **API Root**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

### **5. Test API Endpoints**

Use the interactive Swagger UI to:

- ✅ Browse all available endpoints
- ✅ Test API calls with "Try it out" buttons
- ✅ View request/response examples
- ✅ Understand parameter requirements
- ✅ See error response formats

## 🧪 **Running Tests**

```bash
# Run all tests
python manage.py test

# Run specific test file
python manage.py test lib.tests.test_tasks

# Run with verbose output
python manage.py test lib.tests.test_tasks -v

# Using pytest (alternative)
pytest lib/tests/test_tasks.py -v
```

**Test Results**: 33/33 tests passed (100% success rate)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**John Christian** - [@legilimensjohn](https://github.com/legilimensjohn)

## 🙏 Acknowledgments

- Django REST Framework documentation
- Clean Architecture principles by Robert C. Martin
- RESTful API best practices

---

⭐ Star this repo if you found it helpful!
