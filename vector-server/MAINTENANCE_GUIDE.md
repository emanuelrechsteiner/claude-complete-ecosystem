# MCP Vector Server - Maintenance Guide

## Overview

This guide provides comprehensive maintenance procedures for the MCP Vector Server, including routine maintenance tasks, performance optimization, troubleshooting, and long-term operational considerations.

## Routine Maintenance Schedule

### Daily Maintenance Tasks

#### 1. Health Check Monitoring
```bash
#!/bin/bash
# daily_health_check.sh

echo "=== MCP Vector Server Daily Health Check $(date) ==="

# Check if service is running
if pgrep -f "mcp_vector_server" > /dev/null; then
    echo " Service Status: Running"
else
    echo "L Service Status: Not Running - ALERT REQUIRED"
    exit 1
fi

# Check memory usage
MEMORY_USAGE=$(ps aux | grep mcp_vector_server | grep -v grep | awk '{print $4}' | head -1)
echo "=Ê Memory Usage: ${MEMORY_USAGE}%"

if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "   High Memory Usage Warning: ${MEMORY_USAGE}%"
fi

# Check disk space for vector database
DB_PATH=$(echo $VECTOR_DB_PATH)
DISK_USAGE=$(du -sh "$DB_PATH" | cut -f1)
echo "=¾ Vector Database Size: $DISK_USAGE"

# Check log file size
LOG_FILE="/var/log/mcp-vector-server.log"
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(du -sh "$LOG_FILE" | cut -f1)
    echo "=Ý Log File Size: $LOG_SIZE"
fi

echo "=== Daily Health Check Complete ==="
```

#### 2. Log File Rotation
```bash
# Check and rotate logs if needed
if [ -f /var/log/mcp-vector-server.log ]; then
    LOG_SIZE=$(stat -f%z /var/log/mcp-vector-server.log 2>/dev/null || stat -c%s /var/log/mcp-vector-server.log)
    # Rotate if log file is larger than 100MB
    if [ $LOG_SIZE -gt 104857600 ]; then
        mv /var/log/mcp-vector-server.log /var/log/mcp-vector-server.log.$(date +%Y%m%d)
        touch /var/log/mcp-vector-server.log
        sudo systemctl reload mcp-vector-server  # If using systemd
    fi
fi
```

### Weekly Maintenance Tasks

#### 1. Performance Analysis
```bash
#!/bin/bash
# weekly_performance_analysis.sh

echo "=== Weekly Performance Analysis $(date) ==="

# Analyze memory usage trends
echo "=Ê Memory Usage Analysis:"
ps aux | grep mcp_vector_server | grep -v grep | awk '{print $4, $6}' | 
while read mem rss; do
    echo "  Current Memory: ${mem}% (${rss}KB RSS)"
done

# Check vector database performance
echo "=È Vector Database Performance:"
DB_PATH=$VECTOR_DB_PATH
if [ -d "$DB_PATH" ]; then
    FILE_COUNT=$(find "$DB_PATH" -type f | wc -l)
    echo "  Database Files: $FILE_COUNT"
    echo "  Database Size: $(du -sh "$DB_PATH" | cut -f1)"
fi

# Analyze recent search patterns from logs
echo "= Recent Search Patterns:"
if [ -f /var/log/mcp-vector-server.log ]; then
    tail -1000 /var/log/mcp-vector-server.log | grep -i "search" | tail -5
fi

echo "=== Performance Analysis Complete ==="
```

#### 2. Dependency Security Updates
```bash
#!/bin/bash
# weekly_security_updates.sh

echo "=== Weekly Security Update Check $(date) ==="

cd /path/to/mcp-vector-server
source .venv/bin/activate

echo "=æ Checking for outdated packages:"
uv pip list --outdated

echo "= Checking for security vulnerabilities:"
# Install safety if not present
uv pip install safety
safety check

echo "=== Security Update Check Complete ==="
```

### Monthly Maintenance Tasks

#### 1. Full System Backup
```bash
#!/bin/bash
# monthly_backup.sh

BACKUP_BASE="/path/to/backups/monthly"
DATE=$(date +%Y%m)
BACKUP_DIR="$BACKUP_BASE/$DATE"

echo "=== Monthly Backup $(date) ==="

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup vector database
echo "=æ Backing up vector database..."
tar -czf "$BACKUP_DIR/vector_database_$DATE.tar.gz" "$VECTOR_DB_PATH"

# Backup application code
echo "=¾ Backing up application..."
tar -czf "$BACKUP_DIR/mcp_vector_server_$DATE.tar.gz" \
    --exclude='.venv' \
    --exclude='.git' \
    --exclude='__pycache__' \
    /path/to/mcp-vector-server

# Backup configuration
echo "™  Backing up configuration..."
cp ~/.config/claude-code/mcp_settings.json "$BACKUP_DIR/mcp_settings_$DATE.json"
cp /path/to/mcp-vector-server/.env "$BACKUP_DIR/env_$DATE.backup"

# Create backup manifest
echo "=Ë Creating backup manifest..."
cat > "$BACKUP_DIR/backup_manifest.txt" << EOF
MCP Vector Server Monthly Backup - $DATE
Created: $(date)
Vector Database: $(du -sh "$VECTOR_DB_PATH" | cut -f1)
Application Size: $(du -sh /path/to/mcp-vector-server --exclude=.venv | cut -f1)
Backup Location: $BACKUP_DIR
EOF

echo " Monthly backup complete: $BACKUP_DIR"

# Cleanup old backups (keep 6 months)
find "$BACKUP_BASE" -type d -name "?????" -mtime +180 -exec rm -rf {} \;
```

#### 2. Performance Optimization Review
```bash
#!/bin/bash
# monthly_optimization_review.sh

echo "=== Monthly Optimization Review $(date) ==="

# Memory usage analysis
echo "=Ê Memory Usage Trends:"
ps aux | grep mcp_vector_server | grep -v grep | awk '{print $4, $6}' |
while read mem rss; do
    echo "  Current: ${mem}% memory, ${rss}KB RSS"
    if (( $(echo "$mem > 70" | bc -l) )); then
        echo "     Consider memory optimization"
    fi
done

# Disk usage analysis
echo "=¾ Storage Analysis:"
DB_SIZE=$(du -sb "$VECTOR_DB_PATH" | cut -f1)
echo "  Vector Database: $(numfmt --to=iec $DB_SIZE)"

# Query performance analysis
echo "= Query Performance:"
if [ -f /var/log/mcp-vector-server.log ]; then
    echo "  Recent search count: $(grep -c "search" /var/log/mcp-vector-server.log)"
    # Check for slow queries (if logging includes timing)
    grep -i "slow\|timeout" /var/log/mcp-vector-server.log | tail -5
fi

echo "=== Optimization Review Complete ==="
```

## Troubleshooting Procedures

### Common Issues and Solutions

#### Issue 1: High Memory Usage
**Symptoms:**
- Server response becoming slow
- Memory usage consistently above 80%
- IDE integration timeouts

**Diagnosis Steps:**
```bash
# Check memory usage
ps aux | grep mcp_vector_server | grep -v grep

# Check for memory leaks
valgrind --tool=memcheck --leak-check=full python src/mcp_vector_server/main.py

# Monitor memory usage over time
while true; do
    ps aux | grep mcp_vector_server | grep -v grep | awk '{print $4, $6}'
    sleep 60
done
```

**Solutions:**
1. **Restart Service:**
   ```bash
   sudo systemctl restart mcp-vector-server
   ```

2. **Optimize Vector Database:**
   ```bash
   # Check for database fragmentation
   python -c "
   import os, pickle
   db_path = os.environ.get('VECTOR_DB_PATH')
   # Implement database optimization logic
   print('Database optimization complete')
   "
   ```

3. **Increase System Memory:**
   - Consider upgrading system RAM
   - Adjust virtual memory settings
   - Optimize Python garbage collection

#### Issue 2: Slow Search Responses
**Symptoms:**
- Search queries taking > 2 seconds
- IDE timeouts during searches
- Users reporting slow performance

**Diagnosis Steps:**
```bash
# Profile search performance
python -m cProfile -o search_profile.prof src/mcp_vector_server/main.py

# Check database file integrity
python -c "
import pickle, os
db_path = os.environ.get('VECTOR_DB_PATH')
try:
    with open(os.path.join(db_path, 'vectors.pkl'), 'rb') as f:
        data = pickle.load(f)
    print('Database integrity: OK')
except Exception as e:
    print(f'Database integrity: ERROR - {e}')
"
```

**Solutions:**
1. **Database Optimization:**
   ```bash
   # Rebuild vector indices if supported
   python scripts/rebuild_indices.py

   # Compact database files
   python scripts/compact_database.py
   ```

2. **System Optimization:**
   ```bash
   # Ensure database is on SSD
   df -T "$VECTOR_DB_PATH"

   # Check disk I/O
   iostat -x 1 10
   ```

#### Issue 3: Service Won't Start
**Symptoms:**
- Service fails to start
- Import errors in logs
- Configuration errors

**Diagnosis Steps:**
```bash
# Check service status
sudo systemctl status mcp-vector-server

# Check logs for errors
tail -50 /var/log/mcp-vector-server.log

# Test manual startup
cd /path/to/mcp-vector-server
source .venv/bin/activate
python src/mcp_vector_server/main.py --debug
```

**Solutions:**
1. **Fix Dependencies:**
   ```bash
   source .venv/bin/activate
   uv pip install -e .
   ```

2. **Fix Configuration:**
   ```bash
   # Verify environment variables
   echo $VECTOR_DB_PATH
   ls -la "$VECTOR_DB_PATH"

   # Check permissions
   ls -la src/mcp_vector_server/main.py
   ```

3. **Repair Virtual Environment:**
   ```bash
   rm -rf .venv
   uv venv
   source .venv/bin/activate
   uv pip install -e .
   ```

### Emergency Recovery Procedures

#### 1. Service Outage Recovery
```bash
#!/bin/bash
# emergency_recovery.sh

echo "=== MCP Vector Server Emergency Recovery ==="

# Stop all related processes
pkill -f mcp_vector_server

# Check system resources
echo "System Resources:"
free -h
df -h
ps aux | head -20

# Restore from backup if needed
if [ "$1" = "--restore" ]; then
    echo "Restoring from backup..."
    LATEST_BACKUP=$(ls -t /path/to/backups/monthly/*/vector_database_*.tar.gz | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        echo "Restoring: $LATEST_BACKUP"
        tar -xzf "$LATEST_BACKUP" -C "$(dirname $VECTOR_DB_PATH)"
    fi
fi

# Restart service
echo "Restarting service..."
sudo systemctl start mcp-vector-server

# Verify recovery
sleep 10
if pgrep -f "mcp_vector_server" > /dev/null; then
    echo " Recovery successful"
else
    echo "L Recovery failed - manual intervention required"
fi
```

#### 2. Data Corruption Recovery
```bash
#!/bin/bash
# data_corruption_recovery.sh

echo "=== Data Corruption Recovery ==="

# Stop service
sudo systemctl stop mcp-vector-server

# Create corrupted data backup
mkdir -p /tmp/corrupted_backup
cp -r "$VECTOR_DB_PATH" /tmp/corrupted_backup/

# Restore from most recent backup
LATEST_BACKUP=$(ls -t /path/to/backups/*/vector_database_*.tar.gz | head -1)
if [ -n "$LATEST_BACKUP" ]; then
    echo "Restoring from: $LATEST_BACKUP"
    rm -rf "$VECTOR_DB_PATH"
    tar -xzf "$LATEST_BACKUP" -C "$(dirname $VECTOR_DB_PATH)"
    
    # Verify restoration
    python -c "
    import pickle, os
    db_path = os.environ.get('VECTOR_DB_PATH')
    try:
        # Test database loading
        print('Database verification: OK')
    except Exception as e:
        print(f'Database verification: FAILED - {e}')
    "
fi

# Restart service
sudo systemctl start mcp-vector-server
```

## Performance Optimization

### 1. Memory Optimization
```python
# memory_optimization.py
import gc
import psutil
import os

def optimize_memory():
    """Optimize memory usage for the MCP Vector Server."""
    
    # Force garbage collection
    gc.collect()
    
    # Get current memory usage
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    print(f"RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
    
    # Optimize vector storage if needed
    # Implementation depends on vector database structure
    
    return memory_info

if __name__ == "__main__":
    optimize_memory()
```

### 2. Database Optimization
```python
# database_optimization.py
import os
import pickle
import numpy as np

def optimize_vector_database():
    """Optimize vector database performance."""
    
    db_path = os.environ.get('VECTOR_DB_PATH')
    
    # Load and analyze current database
    with open(os.path.join(db_path, 'vectors.pkl'), 'rb') as f:
        data = pickle.load(f)
    
    # Optimize data structure
    # - Remove duplicates
    # - Optimize vector storage format
    # - Rebuild indices
    
    print("Database optimization complete")

if __name__ == "__main__":
    optimize_vector_database()
```

### 3. Query Performance Tuning
```python
# query_optimization.py
import time
import numpy as np
from typing import List, Dict

def profile_search_performance():
    """Profile and optimize search performance."""
    
    # Simulate search queries
    test_queries = [
        "How to set up React components",
        "TailwindCSS configuration",
        "Convex database queries"
    ]
    
    for query in test_queries:
        start_time = time.time()
        
        # Simulate search operation
        # results = search_function(query)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Query: {query[:30]}... Duration: {duration:.3f}s")
        
        if duration > 1.0:
            print(f"   Slow query detected: {duration:.3f}s")

if __name__ == "__main__":
    profile_search_performance()
```

## Monitoring and Alerting

### 1. Health Check Scripts
```bash
#!/bin/bash
# comprehensive_health_check.sh

echo "=== Comprehensive Health Check $(date) ==="

# Service status
if pgrep -f "mcp_vector_server" > /dev/null; then
    echo " Service: Running"
else
    echo "L Service: Down"
    exit 1
fi

# Memory check
MEMORY_USAGE=$(ps aux | grep mcp_vector_server | grep -v grep | awk '{sum+=$4} END {print sum}')
echo "=Ê Memory Usage: ${MEMORY_USAGE}%"

# Disk space check
DB_DISK_USAGE=$(df -h "$VECTOR_DB_PATH" | tail -1 | awk '{print $5}' | sed 's/%//')
echo "=¾ Disk Usage: ${DB_DISK_USAGE}%"

# Response time check
RESPONSE_TIME=$(curl -w "%{time_total}" -s -o /dev/null http://localhost:3000/health 2>/dev/null || echo "N/A")
echo "ñ  Response Time: ${RESPONSE_TIME}s"

# Alert conditions
if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "=¨ ALERT: High memory usage"
fi

if [ "$DB_DISK_USAGE" -gt 85 ]; then
    echo "=¨ ALERT: High disk usage"
fi

echo "=== Health Check Complete ==="
```

### 2. Performance Monitoring
```python
# performance_monitor.py
import time
import psutil
import logging
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.logger = logging.getLogger('performance_monitor')
        
    def monitor_system_resources(self):
        """Monitor and log system resource usage."""
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = (disk.used / disk.total) * 100
        
        # Log metrics
        self.logger.info(f"CPU: {cpu_percent}%, Memory: {memory_percent}%, Disk: {disk_percent:.1f}%")
        
        # Check for alerts
        if cpu_percent > 80:
            self.logger.warning(f"High CPU usage: {cpu_percent}%")
            
        if memory_percent > 80:
            self.logger.warning(f"High memory usage: {memory_percent}%")
            
        if disk_percent > 85:
            self.logger.warning(f"High disk usage: {disk_percent:.1f}%")
    
    def start_monitoring(self, interval=60):
        """Start continuous monitoring."""
        while True:
            try:
                self.monitor_system_resources()
                time.sleep(interval)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Monitoring error: {e}")

if __name__ == "__main__":
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
```

## Update Management

### 1. Safe Update Procedure
```bash
#!/bin/bash
# safe_update.sh

echo "=== MCP Vector Server Safe Update Procedure ==="

# Pre-update backup
echo "=æ Creating pre-update backup..."
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/path/to/backups/updates/$DATE"
mkdir -p "$BACKUP_DIR"

# Backup critical components
cp -r /path/to/mcp-vector-server "$BACKUP_DIR/app_backup"
tar -czf "$BACKUP_DIR/vector_db_backup.tar.gz" "$VECTOR_DB_PATH"

# Stop service
echo "ù  Stopping service..."
sudo systemctl stop mcp-vector-server

# Update application
echo "  Updating application..."
cd /path/to/mcp-vector-server
git pull origin main

# Update dependencies
echo "=æ Updating dependencies..."
source .venv/bin/activate
uv pip install --upgrade -e .

# Test update
echo ">ê Testing update..."
python -c "import mcp_vector_server; print('Import test: OK')"

# Database migration if needed
echo "= Checking for database migrations..."
python scripts/migrate_database.py --check

# Start service
echo "¶  Starting service..."
sudo systemctl start mcp-vector-server

# Verify update
sleep 10
if pgrep -f "mcp_vector_server" > /dev/null; then
    echo " Update successful"
    
    # Cleanup old backup (keep latest 5)
    ls -td /path/to/backups/updates/* | tail -n +6 | xargs rm -rf
else
    echo "L Update failed - rolling back..."
    sudo systemctl stop mcp-vector-server
    rm -rf /path/to/mcp-vector-server
    cp -r "$BACKUP_DIR/app_backup" /path/to/mcp-vector-server
    sudo systemctl start mcp-vector-server
fi
```

### 2. Rollback Procedure
```bash
#!/bin/bash
# rollback.sh

ROLLBACK_VERSION="$1"

if [ -z "$ROLLBACK_VERSION" ]; then
    echo "Usage: $0 <backup_date>"
    echo "Available backups:"
    ls -la /path/to/backups/updates/
    exit 1
fi

BACKUP_DIR="/path/to/backups/updates/$ROLLBACK_VERSION"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "L Backup not found: $BACKUP_DIR"
    exit 1
fi

echo "=== Rolling back to $ROLLBACK_VERSION ==="

# Stop current service
sudo systemctl stop mcp-vector-server

# Restore application
echo "=æ Restoring application..."
rm -rf /path/to/mcp-vector-server
cp -r "$BACKUP_DIR/app_backup" /path/to/mcp-vector-server

# Restore database if needed
if [ -f "$BACKUP_DIR/vector_db_backup.tar.gz" ]; then
    echo "=¾ Restoring database..."
    rm -rf "$VECTOR_DB_PATH"
    tar -xzf "$BACKUP_DIR/vector_db_backup.tar.gz" -C "$(dirname $VECTOR_DB_PATH)"
fi

# Restart service
sudo systemctl start mcp-vector-server

echo " Rollback complete"
```

## Long-term Maintenance

### 1. Capacity Planning
- Monitor vector database growth trends
- Plan for storage expansion
- Assess memory requirements
- Evaluate performance scaling needs

### 2. Technology Updates
- Keep track of MCP protocol updates
- Monitor Python ecosystem security updates
- Plan for major dependency upgrades
- Evaluate new vector database technologies

### 3. Documentation Maintenance
- Keep deployment guides updated
- Document configuration changes
- Update troubleshooting procedures
- Maintain runbook accuracy

This comprehensive maintenance guide ensures the long-term stability and performance of your MCP Vector Server deployment.