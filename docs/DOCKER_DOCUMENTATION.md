# DPU Performance Studio - Docker Documentation

## Overview

This document provides comprehensive instructions for running the DPU Performance Studio using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

### Development Environment

```bash
# Clone the repository
git clone <repository-url>
cd dpu-performance-studio

# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production Environment

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up --build -d

# Access the application
# Frontend: http://localhost:80
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Docker Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                  dpu-network (bridge)                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────────┐        ┌──────────────────┐  │
│  │   Frontend Container │        │ Backend Container│  │
│  │                      │        │                  │  │
│  │  - Nginx (port 80)   │◄──────►│  - FastAPI       │  │
│  │  - React Build       │  :80   │  - Python 3.11   │  │
│  │  - Static Files      │        │  - Port 8000     │  │
│  │                      │        │                  │  │
│  └──────────────────────┘        └──────────────────┘  │
│         Port 3000                       Port 8000        │
└─────────────────────────────────────────────────────────┘
```

## Services

### Backend Service

**Image:** Built from `backend/Dockerfile`

**Base Image:** `python:3.13-slim`

**Port:** 8000

**Environment Variables:**
- `PYTHONUNBUFFERED=1` - Ensures Python output is not buffered

**Volumes (Development):**
- `./backend:/app` - Live code mounting for development
- `/app/__pycache__` - Excludes Python cache

**Health Check:**
- Test: `curl -f http://localhost:8000/health`
- Interval: 30s
- Timeout: 10s
- Retries: 3
- Start Period: 40s

**Build Context:** `./backend`

### Frontend Service

**Image:** Built from `frontend/Dockerfile` (multi-stage build)

**Base Image:** `node:18-alpine` (builder), `nginx:alpine` (production)

**Port:** 80 (development: 3000, production: 80)

**Depends On:** backend

**Build Context:** `./frontend`

**Nginx Configuration:**
- Serves static React build
- Proxies `/api/*` requests to backend
- Enables gzip compression
- Implements security headers
- Caches static assets

## Docker Compose Files

### docker-compose.yml (Development)

Development configuration with:
- Live code mounting for backend
- Exposed ports: 3000 (frontend), 8000 (backend)
- No volume mounting for frontend (rebuild required)
- Restart policy: `unless-stopped`

### docker-compose.prod.yml (Production)

Production configuration with:
- No code mounting (optimized images)
- Exposed ports: 80 (frontend), 8000 (backend)
- Health check dependency for frontend
- Restart policy: `always`
- Log rotation (max 10MB, 3 files)
- Production environment variable

## Dockerfiles

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Features:**
- Minimal Python image for smaller size
- System dependencies for PyTorch compilation
- Layer caching for faster builds
- Non-root execution support
- Explicit port exposure

### Frontend Dockerfile (Multi-stage)

```dockerfile
# Builder stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Features:**
- Multi-stage build for smaller final image
- Alpine Linux for minimal size
- Nginx for efficient static file serving
- Production-optimized build
- No development dependencies in final image

## Common Docker Commands

### Build Services

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Rebuild without cache
docker-compose build --no-cache
```

### Start Services

```bash
# Start all services in foreground
docker-compose up

# Start all services in background
docker-compose up -d

# Start specific service
docker-compose up backend
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Stop with production config
docker-compose -f docker-compose.prod.yml down
```

### View Logs

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

### Execute Commands in Containers

```bash
# Access backend container shell
docker-compose exec backend bash

# Run Python script in backend
docker-compose exec backend python script.py

# Access frontend container shell
docker-compose exec frontend sh

# Test backend health
docker-compose exec backend curl http://localhost:8000/health
```

### Monitor Services

```bash
# View running containers
docker-compose ps

# View resource usage
docker stats

# View container details
docker inspect dpu-performance-backend
docker inspect dpu-performance-frontend
```

### Clean Up

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove all unused resources
docker system prune -a
```

## Network Configuration

The application uses a custom bridge network named `dpu-network`.

**Network Details:**
- Driver: bridge
- Services: backend, frontend
- Internal DNS: Service names as hostnames
- Backend accessible from frontend as `http://backend:8000`

## Volume Management

### Development Volumes

Backend code is mounted as a bind mount for live development:
- Host: `./backend`
- Container: `/app`

### Production Volumes

No volumes in production (images are self-contained).

### Persistent Data

Currently, no persistent data volumes are needed as the application is stateless.

## Environment Variables

### Backend Environment Variables

- `PYTHONUNBUFFERED=1` - Ensures immediate Python output
- `ENVIRONMENT=production` - (Production only) Sets environment mode

### Adding Custom Environment Variables

Create a `.env` file in the project root:

```env
# Backend
PYTHONUNBUFFERED=1
API_KEY=your_api_key_here

# Frontend (if needed)
REACT_APP_API_URL=http://localhost:8000
```

Update `docker-compose.yml` to use the env file:

```yaml
services:
  backend:
    env_file:
      - .env
```

## Troubleshooting

### Backend Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Port 8000 already in use - Change port in docker-compose.yml
# 2. Python dependencies failing - Check requirements.txt
# 3. Code errors - Check application logs
```

### Frontend Container Won't Start

```bash
# Check logs
docker-compose logs frontend

# Common issues:
# 1. Port 3000/80 already in use - Change port in docker-compose.yml
# 2. Build failure - Check frontend build logs
# 3. Backend not ready - Check backend health
```

### Cannot Access Application

```bash
# Check if containers are running
docker-compose ps

# Check network connectivity
docker-compose exec frontend ping backend

# Check port exposure
docker-compose ps
```

### Build Takes Too Long

```bash
# Use build cache
docker-compose build

# Clear cache if needed
docker-compose build --no-cache

# Use smaller base images (already optimized)
```

### High Memory Usage

```bash
# Check container resource usage
docker stats

# Limit container memory in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 1G
```

## Performance Optimization

### Image Size Optimization

- Use Alpine Linux images (already implemented)
- Multi-stage builds (already implemented)
- Remove unnecessary dependencies
- Use `.dockerignore` files (already implemented)

### Build Time Optimization

- Layer caching (already implemented)
- Copy requirements first (already implemented)
- Use build cache
- Parallel builds (Docker BuildKit)

### Runtime Optimization

- Nginx for static files (already implemented)
- Gzip compression (already implemented)
- Asset caching (already implemented)
- Health checks (already implemented)

## Security Best Practices

### Implemented

- Non-root user support (can be enhanced)
- Minimal base images
- Security headers in Nginx
- No sensitive data in images
- `.dockerignore` to exclude sensitive files

### Additional Recommendations

1. **Scan images for vulnerabilities:**
   ```bash
   docker scan dpu-performance-backend
   docker scan dpu-performance-frontend
   ```

2. **Use specific image tags:**
   ```dockerfile
   FROM python:3.11.7-slim
   FROM node:18.19.0-alpine
   ```

3. **Sign images:**
   ```bash
   docker trust sign dpu-performance-backend:latest
   ```

4. **Run as non-root user:**
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

5. **Read-only filesystem:**
   ```yaml
   services:
     backend:
       read_only: true
       tmpfs:
         - /tmp
   ```

## Deployment

### Deploy to Docker Hub

```bash
# Tag images
docker tag dpu-performance-backend username/dpu-performance-backend:latest
docker tag dpu-performance-frontend username/dpu-performance-frontend:latest

# Push to Docker Hub
docker push username/dpu-performance-backend:latest
docker push username/dpu-performance-frontend:latest
```

### Deploy to Cloud Providers

The Docker Compose configuration can be adapted for:
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- DigitalOcean App Platform
- Heroku (with Docker)

### CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push backend
        run: |
          docker build -t username/dpu-performance-backend ./backend
          docker push username/dpu-performance-backend
      - name: Build and push frontend
        run: |
          docker build -t username/dpu-performance-frontend ./frontend
          docker push username/dpu-performance-frontend
```

## Monitoring and Logging

### Container Logs

```bash
# View logs
docker-compose logs -f

# Log rotation (configured in production)
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Health Monitoring

Health checks are configured for the backend:
- Endpoint: `/health`
- Interval: 30s
- Timeout: 10s
- Retries: 3

### Metrics Integration

Can be integrated with:
- Prometheus + Grafana
- Docker stats
- Cloud provider monitoring

## Backup and Recovery

### Backup Configuration

```bash
# Export docker-compose configuration
docker-compose config > docker-compose-backup.yml

# Backup volumes (if any)
docker run --rm -v dpu-volume:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /data
```

### Recovery

```bash
# Restore configuration
docker-compose -f docker-compose-backup.yml up -d

# Restore volumes
docker run --rm -v dpu-volume:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /
```

## Support

For issues or questions:
1. Check this documentation
2. Review Docker logs: `docker-compose logs`
3. Check container status: `docker-compose ps`
4. Review main project documentation
