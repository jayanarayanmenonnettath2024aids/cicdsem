# AWS Architecture and Deployment Guide

## Complete AWS Setup for Student Management System

### Overview

This guide shows how to deploy the Student Management System using:
- **AWS CodeBuild** - Build and test the application
- **AWS CodePipeline** - Automate the deployment workflow
- **Amazon CloudWatch** - Monitor logs and metrics
- **AWS ECR** - Store Docker images (optional)
- **AWS ECS/EKS** - Run containerized application (advanced)

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Repository                          │
│                    (Source Code)                                │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             │ Webhook
                             ▼
        ┌────────────────────────────────────────┐
        │      AWS CodePipeline                  │
        │  (Orchestrates entire workflow)        │
        └────┬────────────────┬────────────────┬─┘
             │                │                │
        Source          Build Stage      Deploy Stage
             │                │                │
        GitHub        ┌───────▼────────┐      │
             └───────→│ AWS CodeBuild  │      │
                      │ (Test & Build) │      │
                      │ + Docker       │      │
                      │ + pytest       │      │
                      └───────┬────────┘      │
                              │               │
                        ┌─────▼────────┐      │
                        │ CloudWatch   │      │
                        │ Logs         │      │
                        └──────────────┘      │
                                             │
                        ┌────────────────────▼┐
                        │ AWS EC2/ECS/EKS    │
                        │ Running App        │
                        └────────────────────┘
```

---

## Step-by-Step AWS Setup

### Phase 1: Prerequisites (15 minutes)

#### 1. Create AWS Account
- Visit https://aws.amazon.com/
- Click "Create an AWS Account"
- Follow setup wizard
- Add payment method

#### 2. Create IAM User
```
AWS Console → IAM → Users → Add user

Username: student-management-cicd

Attach Permissions:
- AWSCodeBuildAdminAccess
- AWSCodePipelineFullAccess
- CloudWatchLogsFullAccess
- AmazonS3FullAccess
- AmazonEC2ContainerRegistryPowerUser
```

#### 3. Generate Access Keys
```
IAM User → Security credentials → Create access key

Save:
- Access Key ID
- Secret Access Key
```

#### 4. Configure AWS CLI
```bash
pip install awscli

aws configure
# AWS Access Key ID: [YOUR_ACCESS_KEY]
# AWS Secret Access Key: [YOUR_SECRET_KEY]
# Default region: us-east-1
# Default output format: json

# Verify
aws sts get-caller-identity
```

---

### Phase 2: AWS CodeBuild Setup (20 minutes)

#### 1. Create S3 Bucket for Artifacts
```bash
aws s3 mb s3://student-management-artifacts-$(date +%s) --region us-east-1
```

#### 2. Create CodeBuild Project
```
AWS Console → CodeBuild → Create build project

Project Configuration:
  Project name: student-management-ci
  Description: CI/CD for Student Management System

Source:
  Source provider: GitHub
  Repository: [YOUR_REPO_URL]
  Webhook events: PUSH, PULL_REQUEST

Environment:
  Environment image: Amazon Linux 2
  Compute: 3GB memory, 2vCPU
  Runtime(s): Python
  Runtime version: 3.11
  Service role: Create new role

Buildspec:
  Buildspec name: buildspec.yml
  Build commands: Use buildspec.yml from repository

Logs:
  CloudWatch logs:
    ✓ Enable
    Group name: /aws/codebuild/student-management-ci
    Stream name: build-logs

Click "Create build project"
```

#### 3. Test CodeBuild Manually
```bash
aws codebuild start-build --project-name student-management-ci

# Monitor build
aws codebuild batch-get-builds --ids [BUILD_ID]
```

---

### Phase 3: AWS CodePipeline Setup (15 minutes)

#### 1. Create Pipeline
```
AWS Console → CodePipeline → Create pipeline

Pipeline settings:
  Pipeline name: student-management-pipeline
  Service role: Create new service role
  Artifact store: S3 bucket
  Location: Choose bucket created earlier
  
Click "Next"
```

#### 2. Add Source Stage
```
Stage: Source
  Source provider: GitHub
  Owner: [YOUR_USERNAME]
  Repository: [YOUR_REPO]
  Branch: main
  Webhook: Check "I want to use a GitHub webhook"
  
Click "Next"
```

#### 3. Add Build Stage
```
Stage: Build
  Build provider: AWS CodeBuild
  Project name: student-management-ci
  Build type: Single build
  
Click "Next"
```

#### 4. Add Deploy Stage
```
Skip this step for now
(or configure for ECS/EC2)

Click "Create pipeline"
```

#### 5. Configure Webhook
```
AWS Console → CodePipeline → Pipeline → student-management-pipeline

Edit → Source → Change Details
Verify webhook is configured and active
```

---

### Phase 4: CloudWatch Logs Setup (10 minutes)

#### 1. Create Log Group
```bash
aws logs create-log-group \
  --log-group-name /aws/codebuild/student-management-ci \
  --region us-east-1
```

#### 2. Set Retention Policy
```bash
aws logs put-retention-policy \
  --log-group-name /aws/codebuild/student-management-ci \
  --retention-in-days 7 \
  --region us-east-1
```

#### 3. View Logs
```
AWS Console → CloudWatch → Logs → Log groups

Click "/aws/codebuild/student-management-ci"
View recent builds and their output
```

#### 4. Create CloudWatch Dashboard
```
AWS Console → CloudWatch → Dashboards → Create dashboard

Add widgets:
- CodeBuild success/failure rate
- Build duration trends
- CodePipeline execution status
```

---

### Phase 5: GitHub Integration (10 minutes)

#### 1. Create GitHub Personal Access Token
```
GitHub → Settings → Developer settings → Personal access tokens

Select scopes:
- repo (full)
- admin:repo_hook (full)
- admin:org_hook
- admin:gpg_key

Generate token and save
```

#### 2. Connect GitHub to AWS
```
AWS Console → Developer Tools → Connections → Create connection

Select GitHub
Authorization: Authorize AWS Connector for GitHub
Select repository
```

#### 3. Test Connection
```
Push a test commit to repository:

git add .
git commit -m "Test: trigger pipeline"
git push origin main

Monitor in:
- GitHub → Actions (if GitHub Actions enabled)
- AWS → CodePipeline
```

---

## Advanced AWS Deployments

### Deployment Option 1: EC2 Deployment (Intermediate)

#### 1. Create EC2 Instance
```bash
# Using AWS CLI
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t2.micro \
  --key-name student-management-key \
  --security-group-ids sg-xxxxx

# Via Console:
# AWS Console → EC2 → Instances → Launch Instance
# Ubuntu Server 22.04 LTS
# t2.micro (free tier)
# Security group: Allow SSH, HTTP, HTTPS
```

#### 2. Install Dependencies
```bash
ssh -i ~/student-management-key.pem ubuntu@[PUBLIC_IP]

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python
sudo apt-get install -y python3-pip python3-venv

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone [YOUR_REPO]
cd student-management-ci

# Setup application
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run application
python3 app.py
```

#### 3. Add Deploy Stage to Pipeline
```
AWS Console → CodePipeline → Edit Pipeline

Add Deploy Stage:
  Stage name: Deploy
  Action name: Deploy
  Action provider: AppConfig / CodeDeploy / CloudFormation
  
For EC2: Use CodeDeploy

Create appspec.yaml:
version: 0.0
os: linux
phases:
  install:
    runtime-versions:
      python: 3.11
    commands:
      - pip install -r requirements.txt
  start:
    commands:
      - python app.py &
artifacts:
  files:
    - '**/*'
```

---

### Deployment Option 2: ECS Deployment (Advanced)

#### 1. Create ECR Repository
```bash
aws ecr create-repository --repository-name student-management

# Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin [ECR_URL]

# Build and push image
docker build -t student-management:latest .
docker tag student-management:latest [ECR_URL]/student-management:latest
docker push [ECR_URL]/student-management:latest
```

#### 2. Create ECS Cluster
```
AWS Console → ECS → Clusters → Create cluster

Cluster configuration:
  Cluster name: student-management-cluster
  Infrastructure: AWS Fargate
  
Click "Create"
```

#### 3. Create Task Definition
```
AWS Console → ECS → Task Definitions → Create new task definition

Task definition name: student-management-task
Container name: student-management
Image: [ECR_IMAGE_URL]
Port mappings: 5000

Memory: 512 MB
CPU: 256 units

Create
```

#### 4. Create ECS Service
```
AWS Console → ECS → Clusters → student-management-cluster
→ Services → Create

Service configuration:
  Launch type: Fargate
  Task definition: student-management-task
  Desired count: 1
  
Network:
  VPC: Default
  Subnet: Default
  Security group: Default
  
Load balancing: None (for now)

Create service
```

---

### Deployment Option 3: Kubernetes (Advanced)

#### 1. Create EKS Cluster
```bash
# Install eksctl
pip install eksctl

# Create cluster
eksctl create cluster \
  --name student-management \
  --region us-east-1 \
  --nodegroup-name student-management-ng \
  --node-type t3.micro \
  --nodes 2
```

#### 2. Deploy to Kubernetes
```bash
# Create deployment manifest
cat > deployment.yaml << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: student-management
spec:
  replicas: 2
  selector:
    matchLabels:
      app: student-management
  template:
    metadata:
      labels:
        app: student-management
    spec:
      containers:
      - name: student-management
        image: [ECR_IMAGE_URL]
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: production
EOF

# Apply deployment
kubectl apply -f deployment.yaml

# Create service
kubectl expose deployment student-management \
  --type LoadBalancer \
  --port 80 \
  --target-port 5000

# Get service URL
kubectl get service student-management
```

---

## Monitoring and Management

### CloudWatch Metrics

```bash
# Get CodeBuild metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/CodeBuild \
  --metric-name SuccessfulBuilds \
  --start-time 2024-01-15T00:00:00Z \
  --end-time 2024-01-16T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### Logs Insights Queries

```
# Find all errors
fields @timestamp, @message
| filter @message like /ERROR/
| stats count() by bin(5m)

# Build duration trends
fields @timestamp, @duration
| stats avg(@duration), max(@duration), min(@duration) by bin(1h)

# Test failures
fields @timestamp, @message
| filter @message like /FAILED/
| stats count() as failures by @message
```

### Cost Optimization

```
AWS Console → Cost Management → Cost Explorer

Set up budget alerts:
- CloudWatch budget
- CodeBuild usage
- Data transfer

Savings:
- Use free tier (t2.micro)
- Stop unused resources
- Use spot instances
- Set CloudWatch log retention
```

---

## Troubleshooting

### Build Fails

```
1. Check buildspec.yml syntax
   aws codebuild batch-get-builds --ids [BUILD_ID]

2. View detailed logs
   AWS Console → CodeBuild → Build logs

3. Common issues:
   - Missing dependencies in requirements.txt
   - Syntax errors in Python code
   - Missing environment variables
```

### Pipeline Stuck

```
1. Check CodePipeline status
   AWS Console → CodePipeline → [PIPELINE_NAME]

2. Manually retry stage
   Click "Retry stage execution"

3. Check IAM permissions
   Ensure service role has required permissions
```

### Container Won't Start

```
1. Check CloudWatch logs
   /aws/ecs/student-management-cluster

2. Verify Docker image
   docker run -p 5000:5000 [IMAGE]:latest

3. Check security groups
   Ensure port 5000 is open

4. Verify environment variables
   FLASK_ENV=production
   PORT=5000
```

---

## Cost Estimation (Monthly)

```
Service          | Free Tier | Paid Tier | Cost
─────────────────┼───────────┼───────────┼──────
CodeBuild        | 100 mins  | $0.005/min| ~$5
CodePipeline     | 1 pipeline| $1        | $1
CloudWatch Logs  | 5GB free  | $0.50/GB  | ~$2
EC2 (t2.micro)   | 750 hrs   | $0.0116/hr| Free (trial)
S3 (artifacts)   | 5GB free  | $0.023/GB | Free (small)
─────────────────┴───────────┴───────────┴──────
Total Monthly Cost: ~$8 (mostly CodeBuild)
```

---

## References

- [AWS CodeBuild Documentation](https://docs.aws.amazon.com/codebuild/)
- [AWS CodePipeline Documentation](https://docs.aws.amazon.com/codepipeline/)
- [AWS CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS EKS Documentation](https://docs.aws.amazon.com/eks/)

---

For quick start, follow Phase 1-4 (Basic Setup).
For production deployment, follow all phases and choose deployment option.
