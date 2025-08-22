# MCP Vector Server - Deployment Guide

## Overview

This guide provides comprehensive instructions for deploying the MCP Vector Server in production environments. The server is designed to integrate with IDE environments (Claude Code, Cursor, VS Code) and provide semantic search capabilities across technical documentation.

## Prerequisites

### System Requirements
- **Operating System**: macOS, Linux, or Windows with WSL2
- **Python Version**: 3.9 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended for large document collections)
- **Storage**: 2GB for application + storage space for vector database
- **Network**: Internet access for initial setup and dependency installation

### Development Tools
- **UV Package Manager**: For Python environment management
- **Git**: For version control and deployment
- **Text Editor/IDE**: For configuration file editing

## Installation Methods

### Method 1: Local Development Installation

#### Step 1: Clone Repository
```bash
# Clone to your preferred location
git clone <repository-url>
cd mcp-vector-server

# Or if already downloaded, navigate to directory
cd /path/to/mcp-vector-server
```

#### Step 2: Environment Setup
```bash
# Create virtual environment using UV
uv venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -e .
```

#### Step 3: Verify Installation
```bash
# Test the installation
python -c "import mcp_vector_server; print('Installation successful')"
```

### Method 2: Production Deployment

#### Step 1: System User Setup
```bash
# Create dedicated user for the service (Linux/macOS)
sudo useradd -m -s /bin/bash mcpvector
sudo su - mcpvector

# Set up directory structure
mkdir -p ~/mcp-vector-server
cd ~/mcp-vector-server
```

#### Step 2: Application Deployment
```bash
# Clone and install application
git clone <repository-url> .
uv venv --python 3.9
source .venv/bin/activate
uv pip install -e .

# Set appropriate permissions
chmod +x src/mcp_vector_server/main.py
```

## Configuration

### Environment Variables

Create a `.env` file in your project root:

```env
# Vector Database Configuration
VECTOR_DB_PATH="/path/to/your/vector/database"

# Server Configuration
MCP_SERVER_HOST="localhost"
MCP_SERVER_PORT="3000"

# Logging Configuration
LOG_LEVEL="INFO"
LOG_FILE="/path/to/logs/mcp-vector-server.log"

# Performance Settings
MAX_SEARCH_RESULTS=100
DEFAULT_SIMILARITY_THRESHOLD=0.7
CACHE_TTL=3600

# Security Settings (if applicable)
API_KEY_REQUIRED=false
ALLOWED_HOSTS="localhost,127.0.0.1"
```

### Required Configuration Files

#### 1. Vector Database Path Setup
```bash
# Ensure the vector database directory exists and is accessible
export VECTOR_DB_PATH="/Volumes/NvME-Satechi/VectorDatabase/Documentation/2025_Emanuels_Tech_Stack_Docs_VektorDB"

# Verify database files exist
ls -la "$VECTOR_DB_PATH"
# Should show vector database files (.pkl or similar)
```

#### 2. IDE Configuration Files

**For Claude Code** - Add to MCP settings (`~/.config/claude-code/mcp_settings.json`):
```json
{
  "mcpServers": {
    "vector-docs": {
      "command": "python",
      "args": ["/path/to/mcp-vector-server/src/mcp_vector_server/main.py"],
      "env": {
        "VECTOR_DB_PATH": "/path/to/your/vector/database",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

**For Cursor** - Add to settings.json:
```json
{
  "mcp.servers": {
    "vector-docs": {
      "command": "python",
      "args": ["/path/to/mcp-vector-server/src/mcp_vector_server/main.py"],
      "env": {
        "VECTOR_DB_PATH": "/path/to/your/vector/database"
      }
    }
  }
}
```

**For VS Code with MCP Extension**:
```json
{
  "mcp.servers": [
    {
      "name": "vector-docs",
      "command": "python",
      "args": ["/path/to/mcp-vector-server/src/mcp_vector_server/main.py"],
      "env": {
        "VECTOR_DB_PATH": "/path/to/your/vector/database"
      }
    }
  ]
}
```

## Production Deployment Options

### Option 1: Systemd Service (Linux)

Create `/etc/systemd/system/mcp-vector-server.service`:
```ini
[Unit]
Description=MCP Vector Server
After=network.target

[Service]
Type=simple
User=mcpvector
Group=mcpvector
WorkingDirectory=/home/mcpvector/mcp-vector-server
Environment=PATH=/home/mcpvector/mcp-vector-server/.venv/bin
ExecStart=/home/mcpvector/mcp-vector-server/.venv/bin/python src/mcp_vector_server/main.py
Restart=always
RestartSec=3
Environment=VECTOR_DB_PATH="/path/to/vector/database"
Environment=LOG_LEVEL="INFO"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable mcp-vector-server
sudo systemctl start mcp-vector-server
sudo systemctl status mcp-vector-server
```

### Option 2: Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install UV and dependencies
RUN pip install uv
RUN uv venv && uv pip install -e .

# Expose port (if needed for future web interface)
EXPOSE 3000

# Set environment variables
ENV PYTHONPATH=/app
ENV VECTOR_DB_PATH=/app/data/vector_db

# Create data directory
RUN mkdir -p /app/data

# Run the MCP server
CMD [".venv/bin/python", "src/mcp_vector_server/main.py"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  mcp-vector-server:
    build: .
    container_name: mcp-vector-server
    restart: unless-stopped
    volumes:
      - ./data:/app/data
      - /path/to/vector/database:/app/data/vector_db:ro
    environment:
      - VECTOR_DB_PATH=/app/data/vector_db
      - LOG_LEVEL=INFO
    networks:
      - mcp-network

networks:
  mcp-network:
    driver: bridge
```

### Option 3: Process Manager (PM2)

Install PM2:
```bash
npm install -g pm2
```

Create `ecosystem.config.js`:
```javascript
module.exports = {
  apps: [{
    name: 'mcp-vector-server',
    script: 'src/mcp_vector_server/main.py',
    interpreter: '.venv/bin/python',
    cwd: '/path/to/mcp-vector-server',
    env: {
      VECTOR_DB_PATH: '/path/to/vector/database',
      LOG_LEVEL: 'INFO'
    },
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G'
  }]
};
```

Start with PM2:
```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Security Considerations

### 1. File Permissions
```bash
# Secure the application directory
chmod 755 /path/to/mcp-vector-server
chmod 644 /path/to/mcp-vector-server/src/mcp_vector_server/*.py

# Secure configuration files
chmod 600 .env

# Secure vector database (read-only for application)
chmod 644 /path/to/vector/database/*
```

### 2. Network Security
- Run on localhost (127.0.0.1) by default
- Use firewall rules to restrict access if needed
- Consider VPN access for remote development

### 3. Data Protection
```bash
# Backup vector database regularly
cp -r /path/to/vector/database /path/to/backups/$(date +%Y%m%d)

# Set up log rotation
sudo logrotate -d /etc/logrotate.d/mcp-vector-server
```

## Monitoring and Logging

### Log Configuration
```python
# Add to your environment or configuration
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': '/var/log/mcp-vector-server.log',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
```

### Health Monitoring
Create a simple health check script:
```bash
#!/bin/bash
# health_check.sh

# Check if process is running
if pgrep -f "mcp_vector_server" > /dev/null; then
    echo " MCP Vector Server is running"
    exit 0
else
    echo "L MCP Vector Server is not running"
    exit 1
fi
```

### Performance Monitoring
```bash
# Monitor memory usage
ps aux | grep mcp_vector_server

# Monitor log files
tail -f /var/log/mcp-vector-server.log

# Check disk space for vector database
du -sh /path/to/vector/database
```

## Troubleshooting

### Common Issues

#### Issue 1: Vector Database Not Found
```bash
Error: Could not load vector database from path: /path/to/vector/database
```
**Solution:**
1. Verify the path exists: `ls -la /path/to/vector/database`
2. Check file permissions: `ls -la /path/to/vector/database/*`
3. Ensure VECTOR_DB_PATH environment variable is set correctly

#### Issue 2: Python Module Import Errors
```bash
ModuleNotFoundError: No module named 'mcp_vector_server'
```
**Solution:**
1. Activate virtual environment: `source .venv/bin/activate`
2. Reinstall in development mode: `uv pip install -e .`
3. Check PYTHONPATH: `echo $PYTHONPATH`

#### Issue 3: Permission Denied Errors
```bash
PermissionError: [Errno 13] Permission denied
```
**Solution:**
1. Check file ownership: `ls -la src/mcp_vector_server/`
2. Fix permissions: `chmod +x src/mcp_vector_server/main.py`
3. Ensure user has read access to vector database

### Debugging Steps

#### 1. Verbose Logging
```bash
export LOG_LEVEL=DEBUG
python src/mcp_vector_server/main.py
```

#### 2. Test Configuration
```bash
# Test vector database loading
python -c "
import os
from mcp_vector_server import load_vector_database
db_path = os.environ.get('VECTOR_DB_PATH')
print(f'Loading database from: {db_path}')
db = load_vector_database(db_path)
print('Database loaded successfully')
"
```

#### 3. IDE Integration Testing
```bash
# Test MCP protocol communication
python src/mcp_vector_server/main.py --test-mode
```

## Performance Optimization

### 1. Memory Management
```bash
# Monitor memory usage
ps aux | grep python | grep mcp_vector_server

# Optimize Python memory usage
export PYTHONOPTIMIZE=1
export PYTHONHASHSEED=0
```

### 2. Vector Database Optimization
- Ensure vector database is stored on SSD for faster access
- Consider database compression for storage efficiency
- Monitor search query performance

### 3. System Optimization
```bash
# Increase file descriptor limits
ulimit -n 4096

# Optimize Python garbage collection
export PYTHONGC=1
```

## Backup and Recovery

### 1. Vector Database Backup
```bash
#!/bin/bash
# backup_vector_db.sh

BACKUP_DIR="/path/to/backups"
DB_PATH="/path/to/vector/database"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup
tar -czf "$BACKUP_DIR/vector_db_backup_$DATE.tar.gz" -C "$(dirname $DB_PATH)" "$(basename $DB_PATH)"
echo "Backup created: vector_db_backup_$DATE.tar.gz"

# Cleanup old backups (keep last 7 days)
find "$BACKUP_DIR" -name "vector_db_backup_*.tar.gz" -mtime +7 -delete
```

### 2. Configuration Backup
```bash
# Backup all configuration files
cp .env .env.backup
cp -r ~/.config/claude-code/mcp_settings.json mcp_settings.backup.json
```

## Updates and Maintenance

### 1. Update Process
```bash
# 1. Backup current installation
cp -r /path/to/mcp-vector-server /path/to/mcp-vector-server.backup

# 2. Update code
cd /path/to/mcp-vector-server
git pull origin main

# 3. Update dependencies
source .venv/bin/activate
uv pip install -e .

# 4. Test update
python -c "import mcp_vector_server; print('Update successful')"

# 5. Restart service
sudo systemctl restart mcp-vector-server  # If using systemd
```

### 2. Dependency Updates
```bash
# Update all dependencies
uv pip install --upgrade -e .

# Check for security updates
uv pip list --outdated
```

This deployment guide provides comprehensive instructions for getting the MCP Vector Server running in production environments with proper security, monitoring, and maintenance procedures.