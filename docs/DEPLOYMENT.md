# Cyber Tonic Deployment Guide

This guide covers various deployment options for Cyber Tonic, from local development to production environments.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Streamlit Community Cloud](#streamlit-community-cloud)
4. [Production Deployment](#production-deployment)
5. [Cloud Platforms](#cloud-platforms)
6. [Security Considerations](#security-considerations)
7. [Monitoring and Maintenance](#monitoring-and-maintenance)

## 🚀 Local Development

### Prerequisites
- Python 3.9+
- Git
- Virtual environment (recommended)

### Quick Start
```bash
# Clone repository
git clone https://github.com/mimimakingthings/cyber_tonic.git
cd cyber_tonic

# Set up environment
python launch.py --setup

# Launch application
python launch.py
```

### Development with Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f cyber-tonic
```

## 🐳 Docker Deployment

### Single Container
```bash
# Build image
docker build -t cyber-tonic .

# Run container
docker run -d \
  --name cyber-tonic \
  -p 8501:8501 \
  -p 8502:8502 \
  -p 8503:8503 \
  -v $(pwd)/data:/app/data \
  cyber-tonic
```

### Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# Start with caching (Redis)
docker-compose --profile cache up -d

# Start with database (PostgreSQL)
docker-compose --profile database up -d

# Start production setup
docker-compose --profile production up -d
```

### Environment Variables
```bash
# .env file
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
POSTGRES_PASSWORD=your_secure_password
REDIS_URL=redis://redis:6379
```

## ☁️ Streamlit Community Cloud

### Deployment Steps
1. **Prepare Repository**
   ```bash
   # Ensure requirements.txt is up to date
   pip freeze > requirements.txt
   
   # Commit all changes
   git add .
   git commit -m "Prepare for Streamlit Cloud deployment"
   git push origin main
   ```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file path: `apps/main.py`
   - Configure secrets if needed

3. **Configuration**
   ```toml
   # .streamlit/config.toml
   [server]
   port = 8501
   enableCORS = false
   enableXsrfProtection = false
   
   [theme]
   primaryColor = "#1f77b4"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   ```

### Limitations
- **File Storage**: Limited to session-based storage
- **Data Persistence**: Use external databases for production
- **Resource Limits**: CPU and memory constraints
- **Custom Domains**: Not supported on free tier

## 🏭 Production Deployment

### Recommended Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Load Balancer │────│   Web Server    │────│   Application   │
│     (Nginx)     │    │   (Streamlit)   │    │   (Cyber Tonic) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐    ┌─────────────────┐
                       │     Cache       │    │    Database     │
                       │    (Redis)      │    │  (PostgreSQL)   │
                       └─────────────────┘    └─────────────────┘
```

### Nginx Configuration
```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server cyber-tonic:8501;
    }
    
    server {
        listen 80;
        server_name your-domain.com;
        
        location / {
            proxy_pass http://streamlit;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # WebSocket support
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### SSL/TLS Setup
```bash
# Generate SSL certificate (Let's Encrypt)
certbot --nginx -d your-domain.com

# Or use self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/private.key -out ssl/certificate.crt
```

## 🌐 Cloud Platforms

### AWS Deployment
```bash
# Using AWS ECS
aws ecs create-service \
  --cluster cyber-tonic-cluster \
  --service-name cyber-tonic-service \
  --task-definition cyber-tonic-task \
  --desired-count 2

# Using AWS App Runner
aws apprunner create-service \
  --service-name cyber-tonic \
  --source-configuration '{
    "ImageRepository": {
      "ImageIdentifier": "your-account.dkr.ecr.region.amazonaws.com/cyber-tonic:latest",
      "ImageConfiguration": {
        "Port": "8501"
      }
    }
  }'
```

### Google Cloud Platform
```bash
# Using Cloud Run
gcloud run deploy cyber-tonic \
  --image gcr.io/your-project/cyber-tonic \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment
```bash
# Using Container Instances
az container create \
  --resource-group cyber-tonic-rg \
  --name cyber-tonic \
  --image your-registry.azurecr.io/cyber-tonic:latest \
  --ports 8501 8502 8503 \
  --dns-name-label cyber-tonic
```

### Heroku Deployment
```bash
# Create Heroku app
heroku create cyber-tonic-app

# Set environment variables
heroku config:set STREAMLIT_SERVER_PORT=8501
heroku config:set STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Deploy
git push heroku main
```

## 🔒 Security Considerations

### Environment Security
```bash
# Use environment variables for secrets
export DATABASE_URL="postgresql://user:pass@host:port/db"
export SECRET_KEY="your-secret-key"
export API_TOKEN="your-api-token"

# Secure file permissions
chmod 600 .env
chmod 700 data/storage
```

### Network Security
- **Firewall**: Restrict access to necessary ports only
- **VPN**: Use VPN for internal deployments
- **SSL/TLS**: Always use HTTPS in production
- **Rate Limiting**: Implement rate limiting for API endpoints

### Data Security
- **Encryption**: Encrypt data at rest and in transit
- **Backups**: Regular automated backups
- **Access Control**: Implement proper authentication
- **Audit Logging**: Log all access and changes

### Container Security
```dockerfile
# Use non-root user
USER cybertonic

# Scan for vulnerabilities
RUN pip-audit --format=json --output=audit.json

# Use specific base image versions
FROM python:3.9-slim@sha256:...
```

## 📊 Monitoring and Maintenance

### Health Checks
```bash
# Application health
curl -f http://localhost:8501/_stcore/health

# API health
curl -f http://localhost:8000/health

# Database connectivity
docker-compose exec postgres pg_isready
```

### Logging
```bash
# View application logs
docker-compose logs -f cyber-tonic

# View nginx logs
docker-compose logs -f nginx

# Log rotation
logrotate /etc/logrotate.d/cyber-tonic
```

### Monitoring Setup
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Backup Strategy
```bash
# Database backup
docker-compose exec postgres pg_dump -U cybertonic cybertonic > backup.sql

# Data backup
tar -czf data-backup-$(date +%Y%m%d).tar.gz data/

# Automated backup script
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec postgres pg_dump -U cybertonic cybertonic > "backup_${DATE}.sql"
tar -czf "data_backup_${DATE}.tar.gz" data/
aws s3 cp "backup_${DATE}.sql" s3://your-backup-bucket/
aws s3 cp "data_backup_${DATE}.tar.gz" s3://your-backup-bucket/
```

### Updates and Maintenance
```bash
# Update application
git pull origin main
docker-compose build --no-cache
docker-compose up -d

# Update dependencies
pip install --upgrade -r requirements.txt
docker-compose build

# Clean up
docker system prune -f
docker volume prune -f
```

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :8501

# Change ports in docker-compose.yml
ports:
  - "8502:8501"  # Use different host port
```

#### Memory Issues
```bash
# Increase memory limits
docker run --memory=2g cyber-tonic

# Or in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
```

#### Data Persistence
```bash
# Check volume mounts
docker-compose exec cyber-tonic ls -la /app/data

# Fix permissions
docker-compose exec cyber-tonic chown -R cybertonic:cybertonic /app/data
```

### Performance Optimization
```bash
# Enable caching
docker-compose --profile cache up -d

# Scale horizontally
docker-compose up -d --scale cyber-tonic=3

# Monitor resources
docker stats cyber-tonic
```

## 📞 Support

For deployment issues:
1. Check the [User Guide](USER_GUIDE.md) for common problems
2. Review Docker logs: `docker-compose logs cyber-tonic`
3. Check system resources and disk space
4. Verify network connectivity and firewall settings
5. Create an issue on GitHub with deployment details

---

**Happy Deploying! 🚀**
