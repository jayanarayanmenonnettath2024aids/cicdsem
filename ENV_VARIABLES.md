# Environment Variables Configuration

## Local Development (.env)

Create a `.env` file in the project root for local development:

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_APP=app.py
DEBUG=True
TESTING=False

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=app.log

# Database (Future use)
DATABASE_URL=sqlite:///students.db
DATABASE_POOL_SIZE=10
DATABASE_ECHO=False

# Security
SECRET_KEY=your-secret-key-here-change-in-production
SESSION_TIMEOUT=3600

# AWS (Optional)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=

# Feature Flags
ENABLE_EMAIL_NOTIFICATIONS=False
ENABLE_ADVANCED_SEARCH=False
ENABLE_STUDENT_EXPORT=False
```

## Production (.env.production)

For production deployment on AWS:

```bash
# Flask Configuration
FLASK_ENV=production
FLASK_APP=app.py
DEBUG=False
TESTING=False

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Logging
LOG_LEVEL=WARNING
LOG_FILE=/var/log/student-management/app.log

# Database
DATABASE_URL=postgresql://user:password@host:5432/student_db
DATABASE_POOL_SIZE=20
DATABASE_ECHO=False

# Security
SECRET_KEY=use-strong-random-key-here
SESSION_TIMEOUT=1800
SECURE_COOKIES=True
HTTPS_REDIRECT=True

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_CLOUDWATCH_ENABLED=True

# Email
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=noreply@company.com
MAIL_PASSWORD=your-app-password

# Feature Flags
ENABLE_EMAIL_NOTIFICATIONS=True
ENABLE_ADVANCED_SEARCH=True
ENABLE_STUDENT_EXPORT=True
```

## Docker Environment (buildspec.yml)

Environment variables set automatically in AWS CodeBuild:

```yaml
env:
  variables:
    FLASK_ENV: production
    PYTHONUNBUFFERED: 1
    AWS_REGION: us-east-1
```

## GitHub Actions Secrets

Add to GitHub repository settings → Secrets:

```
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
DOCKER_USERNAME=your-docker-user
DOCKER_PASSWORD=your-docker-token
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

## Docker Compose Environment (.env.docker)

```bash
# Flask
FLASK_ENV=production
PORT=5000

# Database (if using Docker Compose with DB)
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=student_db
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Logging
LOG_LEVEL=INFO
```

## Loading Environment Variables in Python

```python
import os
from dotenv import load_dotenv

# Load from .env file (development)
load_dotenv()

# Access variables
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
PORT = int(os.getenv('PORT', 5000))

# With defaults
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///app.db')
```

## Security Best Practices

✅ **Do:**
- Use strong random SECRET_KEY in production
- Never commit .env files to version control
- Use environment variables for sensitive data
- Rotate credentials regularly
- Use AWS Secrets Manager for secrets

❌ **Don't:**
- Commit .env files to Git
- Hardcode credentials in code
- Share credentials via Slack/Email
- Use default passwords
- Store secrets in Docker images

## AWS Systems Manager Parameter Store

```bash
# Store parameters securely
aws ssm put-parameter \
  --name "/student-management/db-password" \
  --value "your-secure-password" \
  --type "SecureString"

# Retrieve parameter
aws ssm get-parameter \
  --name "/student-management/db-password" \
  --with-decryption
```

## Reference in Code

```python
# Secure way to get parameters
import boto3

def get_parameter(param_name):
    client = boto3.client('ssm')
    response = client.get_parameter(
        Name=param_name,
        WithDecryption=True
    )
    return response['Parameter']['Value']

# Usage
DB_PASSWORD = get_parameter('/student-management/db-password')
```
