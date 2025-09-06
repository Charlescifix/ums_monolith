# 📡 API Documentation

## Authentication Endpoints

### POST `/api/v1/auth/register/`
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_email_verified": false,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### POST `/api/v1/auth/login/`
Authenticate user credentials.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_email_verified": false,
    "date_joined": "2024-01-01T00:00:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### POST `/api/v1/auth/password-reset/`
Request password reset email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200):**
```json
{
  "message": "If the email exists, a reset link has been sent."
}
```

## User Management Endpoints

**Authentication Required:** All user management endpoints require Bearer token authentication.

**Header:**
```
Authorization: Bearer <access_token>
```

### GET `/api/v1/users/`
Get paginated list of users with optional search.

**Query Parameters:**
- `search` (optional): Search by email, first_name, or last_name
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20)

**Example:**
```
GET /api/v1/users/?search=john&page=1&page_size=10
```

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "date_joined": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "total_count": 50,
    "page_count": 5,
    "current_page": 1,
    "has_next": true,
    "has_previous": false
  }
}
```

### GET `/api/v1/users/{id}/`
Get detailed user information.

**Response (200):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_email_verified": false,
  "date_joined": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z",
  "profile": {
    "bio": "Software developer",
    "avatar": "/media/avatars/user1.jpg",
    "date_of_birth": "1990-01-01",
    "location": "New York",
    "website": "https://johndoe.com",
    "is_public": true,
    "show_email": false
  }
}
```

### PATCH `/api/v1/users/{id}/update/`
Update user information.

**Request Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "is_active": false
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "john@example.com",
  "first_name": "Jane",
  "last_name": "Smith",
  "is_active": false,
  "is_email_verified": false,
  "date_joined": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-01T12:00:00Z",
  "profile": null
}
```

### DELETE `/api/v1/users/{id}/deactivate/`
Soft delete (deactivate) a user.

**Response (200):**
```json
{
  "message": "User deactivated successfully"
}
```

### POST `/api/v1/users/bulk/`
Perform bulk operations on users.

**Request Body:**
```json
{
  "user_ids": [1, 2, 3],
  "operation": "deactivate"
}
```

**Operations:**
- `activate`: Activate selected users
- `deactivate`: Deactivate selected users

**Response (200):**
```json
{
  "message": "Operation completed successfully",
  "affected_users": 3,
  "total_requested": 3
}
```

## Error Responses

### 400 Bad Request
```json
{
  "email": ["This field is required."],
  "password": ["Ensure this field has at least 8 characters."]
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 404 Not Found
```json
{
  "error": "User not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "An internal error occurred"
}
```

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing django-ratelimit for production deployments.

## Versioning

The API uses URL versioning (`/api/v1/`). Future versions will be backwards compatible or provide migration paths.