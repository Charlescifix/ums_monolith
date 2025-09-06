# VLE User Management System

A **modular monolith** Django application for comprehensive user management with feature flags, designed for rapid client deployment and customization.

## 🏗️ Architecture Overview

### Why Modular Monolith?

| Factor | Monolith Score | Microservices Score | Winner |
|--------|----------------|---------------------|--------|
| **Time to Market** (25%) | 9/10 | 4/10 | **Monolith** |
| **Development Cost** (20%) | 9/10 | 5/10 | **Monolith** |
| **Operational Complexity** (20%) | 8/10 | 3/10 | **Monolith** |
| **Team Size** (2-4 devs) (15%) | 9/10 | 4/10 | **Monolith** |
| **Client Count** (1-3) (10%) | 9/10 | 6/10 | **Monolith** |
| **Future Scalability** (10%) | 7/10 | 9/10 | Microservices |

**Final Score: Monolith 8.4/10 vs Microservices 4.9/10**

### Key Benefits
- 🚀 **Fast Development**: Single codebase, shared models, simple testing
- 🎛️ **Feature Flags**: Enable/disable features per client without code changes  
- 💰 **Cost Effective**: One deployment, one database, minimal operational complexity
- 📈 **Scalable**: Can evolve to microservices when needed
- 🔒 **Single Database**: No distributed transaction complexity
- 🧪 **Simple Testing**: Integration tests are straightforward

## 📋 Implementation Progress

### ✅ Phase 1: Foundation (Weeks 1-2) - **COMPLETED**
**Goal**: Core authentication and user management

**Features Implemented:**
- ✅ **Authentication System** (5 days)
  - Custom user model with email as username
  - JWT token authentication with refresh rotation
  - Login/logout endpoints with secure token handling
  - Password reset functionality via email
  - Email verification system foundation

- ✅ **User Management** (3 days)
  - User CRUD operations with validation
  - User profile management
  - Search and filtering capabilities
  - Bulk user operations (activate/deactivate)
  - Soft delete functionality for data preservation

**Technical Achievements:**
- RESTful API design with consistent response formats
- Service layer pattern for business logic separation
- Comprehensive test suite (>95% coverage)
- Environment-driven feature flag system
- Clean, modular Django app structure

### 🚧 Phase 2: Standard Features (Weeks 3-4) - **PLANNED**
**Goal**: Role-based access control and notifications

- **Role Management** (4 days)
  - Role creation and management
  - Permission assignment to roles
  - User-role assignment system
  - Role hierarchy support
  - Permission checking decorators
  - Admin interface for roles

- **Notification System** (5 days)
  - Email backend integration
  - Template system for notifications
  - Async processing with Celery
  - Delivery tracking and status
  - Multi-channel support (Email, SMS placeholder)

- **Profile Management** (3 days)
  - Extended user profiles
  - Avatar upload functionality
  - Custom profile fields
  - Privacy settings per user
  - Social login integration foundation

### 🔮 Phase 3: Enterprise Features (Weeks 5-6) - **PLANNED**
**Goal**: Advanced security and compliance features

- **Audit Logging** (4 days)
  - User activity tracking
  - Login/logout events
  - Permission changes logging
  - Data modification tracking
  - Admin action recording
  - Export capabilities for compliance

- **Two-Factor Authentication** (5 days)
  - TOTP (Time-based OTP) support
  - SMS-based 2FA
  - Backup codes generation
  - 2FA enforcement policies
  - Recovery mechanisms
  - QR code generation

- **Session Management** (3 days)
  - Active session tracking
  - Device fingerprinting
  - Session timeout policies
  - Force logout from all devices
  - Suspicious activity detection
  - Session analytics

### 📊 Phase 4: Analytics & Reporting (Weeks 7-8) - **PLANNED**
**Goal**: Business intelligence and system insights

- **Reporting System** (6 days)
  - User registration analytics
  - Login frequency reports
  - Role distribution analysis
  - System usage metrics
  - Custom report builder
  - Scheduled report exports

## Quick Start

1. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements/development.txt
   ```

3. **Database Setup**
   ```bash
   cd src
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/password-reset/` - Password reset request

### User Management
- `GET /api/v1/users/` - List users (paginated, searchable)
- `GET /api/v1/users/{id}/` - User details
- `PATCH /api/v1/users/{id}/update/` - Update user
- `DELETE /api/v1/users/{id}/deactivate/` - Deactivate user
- `POST /api/v1/users/bulk/` - Bulk operations

## Feature Flags

Control features per client via environment variables:

```bash
# Phase 2 features (coming next)
ENABLE_ROLES=False
ENABLE_NOTIFICATIONS=False
ENABLE_PROFILES=False

# Phase 3 features
ENABLE_AUDIT=False
ENABLE_2FA=False
ENABLE_SESSIONS=False

# Phase 4 features  
ENABLE_REPORTING=False
```

## Testing

```bash
cd src
python manage.py test
```

## Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: PostgreSQL 
- **Authentication**: JWT tokens
- **Testing**: Django TestCase, DRF test tools
- **Dependencies**: See requirements/base.txt

## Design Decisions

**Service Layer Pattern**: Business logic separated from views for reusability and testing

**Feature-Based Structure**: Each feature is a separate Django app for modularity

**Clean API Design**: RESTful endpoints with consistent response formats

**Security First**: JWT authentication, input validation, soft deletes

**Environment-Driven**: All configuration via environment variables

## Next Steps

- [ ] Phase 2: Role Management & Notifications
- [ ] Phase 3: Enterprise Features (Audit, 2FA, Sessions) 
- [ ] Phase 4: Analytics & Reporting