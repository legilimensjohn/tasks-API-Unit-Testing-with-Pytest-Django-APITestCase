# 📚 **Task Management API Documentation**

## 🌟 **API Overview**

Welcome to the Task Management API! This comprehensive REST API provides full CRUD operations for task management with enterprise-grade features and documentation.

### **🔗 Documentation Links**

- **Swagger UI**: http://127.0.0.1:8000/swagger/
- **ReDoc**: http://127.0.0.1:8000/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/swagger.json

---

## 🚀 **Quick Start**

### **Base URL**

```
http://127.0.0.1:8000/api/
```

### **Content-Type**

All requests should use:

```
Content-Type: application/json
```

---

## 📋 **Core Endpoints**

### **1. List All Tasks**

```http
GET /api/tasks/
```

**Query Parameters:**

- `status` (optional): Filter by task status (`pending`, `in_progress`, `completed`)
- `priority` (optional): Filter by priority (`low`, `medium`, `high`)

**Response:** 200 OK

```json
[
  {
    "id": 1,
    "title": "Complete API Documentation",
    "description": "Add comprehensive Swagger docs",
    "priority": "high",
    "status": "in_progress",
    "created_at": "2025-10-27T10:30:00Z",
    "updated_at": "2025-10-27T15:45:00Z",
    "due_date": null
  }
]
```

### **2. Create New Task**

```http
POST /api/tasks/
```

**Request Body:**

```json
{
  "title": "New Task",
  "description": "Task description",
  "priority": "medium",
  "status": "pending"
}
```

**Response:** 201 Created

```json
{
  "id": 2,
  "title": "New Task",
  "description": "Task description",
  "priority": "medium",
  "status": "pending",
  "created_at": "2025-10-27T16:00:00Z",
  "updated_at": "2025-10-27T16:00:00Z",
  "due_date": null
}
```

### **3. Get Task Details**

```http
GET /api/tasks/{id}/
```

**Response:** 200 OK (same format as create)

### **4. Update Task**

```http
PUT /api/tasks/{id}/
```

**Request Body:** (All fields required)

```json
{
  "title": "Updated Task",
  "description": "Updated description",
  "priority": "high",
  "status": "completed"
}
```

### **5. Partial Update**

```http
PATCH /api/tasks/{id}/
```

**Request Body:** (Only changed fields)

```json
{
  "status": "completed"
}
```

### **6. Delete Task**

```http
DELETE /api/tasks/{id}/
```

**Response:** 204 No Content

---

## 🎯 **Business Logic Endpoints**

### **1. High Priority Tasks**

```http
GET /api/tasks/high_priority/
```

Returns all tasks with `priority: "high"`.

### **2. Task Statistics**

```http
GET /api/tasks/statistics/
```

**Response:**

```json
{
  "total_tasks": 15,
  "pending": 5,
  "in_progress": 7,
  "completed": 3,
  "high_priority": 4,
  "medium_priority": 8,
  "low_priority": 3
}
```

### **3. Bulk Update**

```http
POST /api/tasks/bulk_update/
```

**Request Body:**

```json
{
  "task_ids": [1, 2, 3],
  "status": "completed"
}
```

**Response:**

```json
{
  "updated_count": 3,
  "tasks": [
    // Array of updated task objects
  ]
}
```

---

## 🔍 **Filtering Examples**

### **Filter by Status**

```http
GET /api/tasks/?status=pending
```

### **Filter by Priority**

```http
GET /api/tasks/?priority=high
```

### **Multiple Filters**

```http
GET /api/tasks/?status=pending&priority=high
```

---

## 📊 **HTTP Status Codes**

| Code | Description            | Usage                      |
| ---- | ---------------------- | -------------------------- |
| 200  | OK                     | Successful GET, PUT, PATCH |
| 201  | Created                | Successful POST            |
| 204  | No Content             | Successful DELETE          |
| 400  | Bad Request            | Invalid data               |
| 404  | Not Found              | Resource doesn't exist     |
| 405  | Method Not Allowed     | Wrong HTTP method          |
| 415  | Unsupported Media Type | Missing Content-Type       |

---

## 🛠️ **Field Validation**

### **Task Model Fields**

| Field       | Type   | Required | Options                         | Max Length |
| ----------- | ------ | -------- | ------------------------------- | ---------- |
| title       | String | ✅ Yes   | -                               | 200 chars  |
| description | String | ❌ No    | -                               | Unlimited  |
| priority    | String | ✅ Yes   | low, medium, high               | -          |
| status      | String | ✅ Yes   | pending, in_progress, completed | -          |
| due_date    | Date   | ❌ No    | ISO 8601 format                 | -          |

### **Validation Rules**

- **title**: Cannot be empty or only whitespace
- **priority**: Must be one of: `low`, `medium`, `high`
- **status**: Must be one of: `pending`, `in_progress`, `completed`

---

## 🧪 **Testing the API**

### **Using cURL**

```bash
# Create a task
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "high", "status": "pending"}'

# Get all tasks
curl http://127.0.0.1:8000/api/tasks/

# Update a task
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### **Using Python Requests**

```python
import requests

# Base URL
base_url = "http://127.0.0.1:8000/api/tasks/"

# Create task
task_data = {
    "title": "Python API Test",
    "priority": "medium",
    "status": "pending"
}
response = requests.post(base_url, json=task_data)
print(response.json())

# Get all tasks
response = requests.get(base_url)
print(response.json())
```

---

## 🔧 **Development Tools**

### **Interactive Documentation**

- **Swagger UI**: Interactive API explorer with try-it-out functionality
- **ReDoc**: Clean, responsive API documentation

### **Testing**

- Comprehensive test suite with 33 unit tests
- 100% CRUD operation coverage
- Error handling validation

### **Architecture**

- Service layer pattern for business logic
- Serializer validation with custom rules
- ViewSet-based API design
- Comprehensive error responses

---

## 🚨 **Error Handling**

### **Validation Errors (400)**

```json
{
  "errors": {
    "title": ["This field may not be blank."],
    "priority": ["\"invalid\" is not a valid choice."]
  },
  "message": "Validation failed"
}
```

### **Not Found Errors (404)**

```json
{
  "detail": "Not found."
}
```

### **Method Not Allowed (405)**

```json
{
  "detail": "Method \"PATCH\" not allowed."
}
```

---

## 📞 **Support**

For questions or issues:

- Check the interactive Swagger documentation at `/swagger/`
- Review the comprehensive test suite in `lib/tests/test_tasks.py`
- Examine the API source code in `taskapp/views.py`

**Happy coding! 🎉**
