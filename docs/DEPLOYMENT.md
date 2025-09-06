# 🚀 Deployment Guide

## Railway Deployment Setup

### Prerequisites
- Railway account
- PostgreSQL database instance
- GitHub repository

### Environment Variables for Railway

Copy these environment variables to your Railway deployment:

```bash
# Django Configuration
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app

# Database (You'll provide this)
DATABASE_URL=postgresql://user:password@host:port/database

# Feature Flags - Configure per client
ENABLE_ROLES=False
ENABLE_NOTIFICATIONS=False
ENABLE_PROFILES=False
ENABLE_AUDIT=False
ENABLE_2FA=False
ENABLE_SESSIONS=False
ENABLE_REPORTING=False

# Optional: Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Optional: Redis Cache
REDIS_URL=redis://localhost:6379/0
```

### Deployment Steps

1. **Connect GitHub Repository**
   ```bash
   # After pushing to GitHub, connect your repository to Railway
   railway login
   railway link
   ```

2. **Set Environment Variables**
   - Go to Railway dashboard
   - Add all environment variables listed above
   - **Important**: Set `DATABASE_URL` to your PostgreSQL connection string

3. **Deploy**
   ```bash
   # Railway will automatically deploy on git push
   git push origin main
   ```

4. **Run Initial Setup** (First deployment only)
   ```bash
   # Railway will automatically run:
   python src/manage.py migrate
   python src/manage.py collectstatic --noinput
   ```

5. **Create Superuser** (Optional)
   ```bash
   railway run python src/manage.py createsuperuser
   ```

### Client Customization via Feature Flags

Each client deployment can have different features enabled:

#### Client 1 - Basic Package
```bash
ENABLE_ROLES=False
ENABLE_NOTIFICATIONS=False
ENABLE_PROFILES=False
```

#### Client 2 - Standard Package  
```bash
ENABLE_ROLES=True
ENABLE_NOTIFICATIONS=True
ENABLE_PROFILES=True
```

#### Client 3 - Enterprise Package
```bash
ENABLE_ROLES=True
ENABLE_NOTIFICATIONS=True
ENABLE_PROFILES=True
ENABLE_AUDIT=True
ENABLE_2FA=True
ENABLE_SESSIONS=True
ENABLE_REPORTING=True
```

### Health Checks

Your deployment will be available at:
- **API Health**: `https://your-app.railway.app/api/v1/auth/`
- **Admin Panel**: `https://your-app.railway.app/admin/`

### Troubleshooting

**Common Issues:**

1. **Database Connection Error**
   - Verify `DATABASE_URL` is correctly formatted
   - Ensure PostgreSQL instance is accessible

2. **Static Files Not Loading**
   - Check `ALLOWED_HOSTS` includes your Railway domain
   - Verify `collectstatic` ran successfully

3. **Environment Variables**
   - Double-check all required env vars are set
   - Restart deployment after changing env vars

### Monitoring

Railway provides:
- ✅ Automatic deployments from GitHub
- ✅ Built-in logs and metrics
- ✅ Health checks
- ✅ SSL certificates
- ✅ Custom domains

### Scaling

For high-traffic clients:
1. Upgrade Railway plan for more resources
2. Enable Redis caching with `REDIS_URL`
3. Consider read replicas for database
4. Monitor performance metrics in Railway dashboard