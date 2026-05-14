# Installation and Quick Start Guide

## Quick Start (5 minutes)

### 1. Install Python Dependencies
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
# Visit http://localhost:5000/
```

### 3. Run Tests
```bash
pytest tests/ -v
```

### 4. Run with Docker
```bash
docker build -t student-management:latest .
docker run -p 5000:5000 student-management:latest
```

---

## Full Setup Guide

### Prerequisites
- Python 3.9+
- Git
- Docker (optional)
- AWS Account (optional)

### Step-by-Step

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd student-management-ci
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Tests**
   ```bash
   pytest tests/ -v
   ```

5. **Start Application**
   ```bash
   python app.py
   ```

6. **Access Application**
   - Open browser to http://localhost:5000/
   - Click through the interface

---

## AWS Setup

### Prerequisites
- AWS Account
- AWS CLI configured
- IAM user with permissions

### Setup Steps

1. **Create CodeBuild Project**
   - Navigate to AWS CodeBuild
   - Create project: `student-management-ci`
   - Use buildspec.yml from repository
   - Configure environment (Amazon Linux 2, Python)

2. **Create CodePipeline**
   - Navigate to AWS CodePipeline
   - Create pipeline
   - Add GitHub source (main branch)
   - Add CodeBuild stage
   - Create pipeline

3. **Enable CloudWatch Logs**
   - Create log group: `/aws/codebuild/student-management-ci`
   - Set retention period

4. **Test Pipeline**
   - Push code to GitHub
   - Watch pipeline in AWS Console
   - Check CloudWatch logs

---

## GitHub Actions Setup

1. **Add Secrets to GitHub**
   - Settings → Secrets and variables → Actions
   - Add: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
   - Add: DOCKER_USERNAME, DOCKER_PASSWORD (optional)
   - Add: SLACK_WEBHOOK_URL (optional)

2. **Enable Actions**
   - Go to Actions tab
   - Click "I understand my workflows, go ahead and enable them"

3. **Test Workflow**
   - Push code to main branch
   - Watch Actions tab for workflow execution

---

## Troubleshooting

### Issue: Module not found
**Solution:** `pip install -r requirements.txt`

### Issue: Port already in use
**Solution:** `kill -9 $(lsof -t -i:5000)` or use different port

### Issue: Tests fail
**Solution:** Ensure database file is deleted, run: `rm students_db.json`

### Issue: Docker build fails
**Solution:** `docker system prune -a` then rebuild

---

## Resources

- **Documentation**: See README.md
- **Tests**: Run with `pytest tests/ -v`
- **API Docs**: See README.md API section
- **Learning**: Check README.md Learning Resources section

For more information, see the full README.md file.
