# Security Documentation

## Overview

DocScraper handles sensitive data including API keys, scraped content, and potentially proprietary documentation. This document outlines security best practices, threat models, and mitigation strategies.

## Secrets Management

### API Key Storage

**Never commit API keys to version control!**

#### Secure Storage Pattern
```python
# .env file (gitignored)
OPENAI_API_KEY=sk-...your-key-here...

# Python code
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    logger.warning("OpenAI API key not found, LLM features disabled")
```

#### Environment Variable Best Practices
1. **Use .env files**: Store secrets in `.env` files
2. **Add to .gitignore**: Always exclude `.env` from version control
3. **Provide examples**: Include `.env.example` with dummy values
4. **Validate on startup**: Check for required keys early
5. **Use key rotation**: Regularly rotate API keys
6. **Limit scope**: Use keys with minimal required permissions

### Secure Configuration

```python
# config.py - Secure configuration loading
import os
from typing import Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

class SecureConfig:
    """Secure configuration management."""
    
    def __init__(self):
        load_dotenv()
        self._validate_environment()
    
    def _validate_environment(self):
        """Validate required environment variables."""
        required = []  # Add required vars here
        missing = [var for var in required if not os.getenv(var)]
        
        if missing:
            raise EnvironmentError(f"Missing required environment variables: {missing}")
    
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key securely."""
        key = os.getenv('OPENAI_API_KEY')
        if key and key.startswith('sk-'):
            return key
        logger.warning("Invalid or missing OpenAI API key")
        return None
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return os.getenv('ENVIRONMENT', 'development').lower() == 'production'
```

## Web Scraping Ethics and Security

### Respecting robots.txt

```python
import urllib.robotparser
from urllib.parse import urlparse

class RobotsChecker:
    """Check robots.txt compliance."""
    
    def __init__(self):
        self.robots_cache = {}
    
    def can_fetch(self, url: str, user_agent: str = "DocScraper/1.0") -> bool:
        """Check if URL can be fetched according to robots.txt."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        
        if robots_url not in self.robots_cache:
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.robots_cache[robots_url] = rp
            except Exception as e:
                logger.warning(f"Could not read robots.txt: {e}")
                return True  # Assume allowed if can't read
        
        return self.robots_cache[robots_url].can_fetch(user_agent, url)
```

### Rate Limiting

```python
import asyncio
import time
from typing import Dict

class RateLimiter:
    """Implement rate limiting for ethical scraping."""
    
    def __init__(self, max_per_second: float = 2.0, max_per_minute: float = 100.0):
        self.max_per_second = max_per_second
        self.max_per_minute = max_per_minute
        self.requests_per_domain: Dict[str, list] = {}
    
    async def acquire(self, domain: str):
        """Acquire permission to make a request."""
        now = time.time()
        
        if domain not in self.requests_per_domain:
            self.requests_per_domain[domain] = []
        
        # Clean old requests
        self.requests_per_domain[domain] = [
            t for t in self.requests_per_domain[domain]
            if now - t < 60
        ]
        
        # Check rate limits
        recent_requests = self.requests_per_domain[domain]
        
        # Per-second limit
        recent_second = [t for t in recent_requests if now - t < 1]
        if len(recent_second) >= self.max_per_second:
            await asyncio.sleep(1 - (now - recent_second[0]))
        
        # Per-minute limit
        if len(recent_requests) >= self.max_per_minute:
            await asyncio.sleep(60 - (now - recent_requests[0]))
        
        # Record request
        self.requests_per_domain[domain].append(time.time())
```

### User Agent Identification

```python
# Always identify your scraper
USER_AGENT = "DocScraper/1.0 (https://github.com/yourusername/docscraper)"

# Include contact information for site owners
HEADERS = {
    "User-Agent": USER_AGENT,
    "X-Contact": "your-email@example.com",
    "X-Purpose": "Documentation archival and processing"
}
```

## Authentication and Authorization

### API Authentication Flow

```python
from typing import Optional
import hashlib
import hmac

class APIAuthenticator:
    """Handle API authentication securely."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._validate_key()
    
    def _validate_key(self):
        """Validate API key format."""
        if self.api_key:
            if not self.api_key.startswith(('sk-', 'pk-')):
                raise ValueError("Invalid API key format")
            if len(self.api_key) < 20:
                raise ValueError("API key too short")
    
    def create_headers(self) -> dict:
        """Create authenticated headers."""
        if not self.api_key:
            return {}
        
        return {
            "Authorization": f"Bearer {self.api_key}",
            "X-API-Version": "1.0"
        }
    
    def sign_request(self, payload: str, secret: str) -> str:
        """Sign request payload with HMAC."""
        signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
```

### Permission Boundaries

```python
import os
from pathlib import Path

class FileSystemSecurity:
    """Enforce file system security boundaries."""
    
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir).resolve()
    
    def validate_path(self, path: str) -> Path:
        """Validate path is within allowed directory."""
        target = Path(path).resolve()
        
        # Prevent path traversal
        if not str(target).startswith(str(self.base_dir)):
            raise SecurityError(f"Path traversal attempt: {path}")
        
        # Check for sensitive files
        if target.name.startswith('.'):
            raise SecurityError(f"Hidden file access denied: {path}")
        
        return target
    
    def safe_write(self, path: str, content: str):
        """Safely write file within boundaries."""
        target = self.validate_path(path)
        
        # Create parent directories safely
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # Write with restricted permissions
        target.write_text(content)
        os.chmod(target, 0o644)  # Read for all, write for owner
```

## Input Validation and Sanitization

### URL Validation

```python
from urllib.parse import urlparse
import re

class URLValidator:
    """Validate and sanitize URLs."""
    
    ALLOWED_SCHEMES = ['http', 'https']
    BLOCKED_DOMAINS = ['localhost', '127.0.0.1', '0.0.0.0']
    
    @classmethod
    def validate(cls, url: str) -> str:
        """Validate and sanitize URL."""
        # Basic format check
        if not url or not isinstance(url, str):
            raise ValueError("Invalid URL format")
        
        # Parse URL
        parsed = urlparse(url)
        
        # Check scheme
        if parsed.scheme not in cls.ALLOWED_SCHEMES:
            raise ValueError(f"Unsupported scheme: {parsed.scheme}")
        
        # Block local addresses
        if parsed.netloc in cls.BLOCKED_DOMAINS:
            raise ValueError("Local addresses not allowed")
        
        # Block private IP ranges
        if cls._is_private_ip(parsed.netloc):
            raise ValueError("Private IP addresses not allowed")
        
        # Sanitize URL
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            clean_url += f"?{parsed.query}"
        
        return clean_url
    
    @staticmethod
    def _is_private_ip(host: str) -> bool:
        """Check if host is a private IP address."""
        ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(ip_pattern, host):
            octets = [int(x) for x in host.split('.')]
            # Check private ranges
            if octets[0] == 10:  # 10.0.0.0/8
                return True
            if octets[0] == 172 and 16 <= octets[1] <= 31:  # 172.16.0.0/12
                return True
            if octets[0] == 192 and octets[1] == 168:  # 192.168.0.0/16
                return True
        return False
```

### Content Sanitization

```python
import html
import re
from typing import Optional

class ContentSanitizer:
    """Sanitize scraped content."""
    
    # Patterns that might indicate sensitive data
    SENSITIVE_PATTERNS = [
        r'api[_-]?key\s*[:=]\s*["\']?[\w-]+',
        r'password\s*[:=]\s*["\']?[\w-]+',
        r'token\s*[:=]\s*["\']?[\w-]+',
        r'secret\s*[:=]\s*["\']?[\w-]+',
    ]
    
    @classmethod
    def sanitize_html(cls, content: str) -> str:
        """Sanitize HTML content."""
        # Escape HTML entities
        content = html.escape(content)
        
        # Remove script tags
        content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL)
        
        # Remove inline JavaScript
        content = re.sub(r'on\w+\s*=\s*["\'].*?["\']', '', content)
        
        return content
    
    @classmethod
    def check_sensitive_data(cls, content: str) -> Optional[str]:
        """Check for potential sensitive data."""
        for pattern in cls.SENSITIVE_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                return f"Potential sensitive data detected: {pattern}"
        return None
    
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitize filename to prevent security issues."""
        # Remove path components
        filename = os.path.basename(filename)
        
        # Remove dangerous characters
        filename = re.sub(r'[^\w\-_\.]', '_', filename)
        
        # Limit length
        name, ext = os.path.splitext(filename)
        if len(name) > 200:
            name = name[:200]
        
        return name + ext
```

## Security Risks and Mitigations

### Risk Matrix

| Risk | Severity | Likelihood | Mitigation |
|------|----------|------------|------------|
| API Key Exposure | High | Medium | Environment variables, .gitignore |
| Path Traversal | High | Low | Path validation, sandboxing |
| XSS in Saved Content | Medium | Low | Content sanitization |
| Rate Limit Violations | Low | Medium | Rate limiting, backoff |
| Robots.txt Violations | Low | Medium | robots.txt checking |
| Resource Exhaustion | Medium | Low | Memory limits, timeouts |
| Malicious Content | Medium | Low | Content validation |

### Quick Security Wins

1. **Enable HTTPS Only**
```python
# Force HTTPS for all requests
if not url.startswith('https://'):
    url = url.replace('http://', 'https://')
```

2. **Set Timeouts**
```python
# Prevent hanging requests
TIMEOUT = 30  # seconds
async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as session:
    # Make requests
```

3. **Limit File Sizes**
```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

if response.headers.get('content-length'):
    if int(response.headers['content-length']) > MAX_FILE_SIZE:
        raise ValueError("File too large")
```

4. **Validate Content Types**
```python
ALLOWED_CONTENT_TYPES = ['text/html', 'text/plain', 'text/markdown']

if response.headers.get('content-type') not in ALLOWED_CONTENT_TYPES:
    raise ValueError(f"Unsupported content type: {response.headers.get('content-type')}")
```

5. **Use Temporary Directories**
```python
import tempfile

with tempfile.TemporaryDirectory() as temp_dir:
    # Process files in isolated temporary directory
    # Automatically cleaned up on exit
```

## Security Checklist

### Development

- [ ] API keys in environment variables
- [ ] .env file in .gitignore
- [ ] Input validation on all user inputs
- [ ] Path traversal prevention
- [ ] Content sanitization
- [ ] Error messages don't leak sensitive info
- [ ] Dependencies regularly updated
- [ ] Security headers in HTTP requests

### Deployment

- [ ] Production API keys separate from development
- [ ] HTTPS enforced for all external requests  
- [ ] Rate limiting configured
- [ ] Logging excludes sensitive data
- [ ] File permissions properly set
- [ ] Resource limits configured
- [ ] Monitoring for suspicious activity
- [ ] Regular security audits

### Code Review

- [ ] No hardcoded secrets
- [ ] Proper exception handling
- [ ] Safe file operations
- [ ] URL validation
- [ ] SQL injection prevention (if using DB)
- [ ] XSS prevention
- [ ] CSRF protection (if web interface)
- [ ] Authentication checks

## Incident Response

### If API Key is Exposed

1. **Immediately revoke** the exposed key
2. **Generate new key** from provider dashboard
3. **Update** .env file with new key
4. **Audit logs** for unauthorized usage
5. **Rotate** any other potentially affected keys
6. **Review** git history for other exposures

### If Malicious Content is Detected

1. **Quarantine** the affected files
2. **Log** the incident with details
3. **Scan** other content for similar patterns
4. **Update** sanitization rules
5. **Report** to appropriate parties if needed

## Security Tools

### Dependency Scanning

```bash
# Check for known vulnerabilities
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

### Secret Scanning

```bash
# Scan for secrets in code
pip install detect-secrets
detect-secrets scan --baseline .secrets.baseline
detect-secrets audit .secrets.baseline
```

### Static Analysis

```bash
# Security linting
pip install bandit
bandit -r . -f json -o bandit-report.json
```

## Compliance Considerations

### GDPR Compliance
- Don't scrape personal data without consent
- Implement data deletion capabilities
- Log data processing activities
- Respect opt-out mechanisms

### Copyright Compliance
- Respect copyright notices
- Follow fair use guidelines
- Attribute sources appropriately
- Don't redistribute copyrighted content

### Terms of Service
- Read and comply with website ToS
- Respect API usage limits
- Follow documentation licenses
- Honor rate limit headers