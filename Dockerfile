# Multi-stage Dockerfile for Student Management System
# Stage 1: Builder - Install dependencies and build application
# Stage 2: Runtime - Run application with minimal footprint

# ==================== STAGE 1: BUILDER ====================

FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# ==================== STAGE 2: RUNTIME ====================

FROM python:3.11-slim

# Set metadata
LABEL maintainer="DevOps Team"
LABEL description="Cloud-Based Student Management System"
LABEL version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production \
    PORT=5000

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Set PATH to use local pip packages
ENV PATH=/home/appuser/.local/bin:$PATH

# Create directory for logs
RUN mkdir -p /app/logs && chown -R appuser:appuser /app/logs

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# ==================== ENTRYPOINT ====================

# Use gunicorn in production for better performance and stability
CMD ["gunicorn", \
     "--bind=0.0.0.0:5000", \
     "--workers=4", \
     "--threads=2", \
     "--worker-class=sync", \
     "--access-logfile=-", \
     "--error-logfile=-", \
     "--log-level=info", \
     "app:app"]

# ==================== BUILD INSTRUCTIONS ====================

# Build the Docker image:
# docker build -t student-management:latest .

# Run the Docker container:
# docker run -d -p 5000:5000 --name student-app student-management:latest

# View logs:
# docker logs student-app

# Stop the container:
# docker stop student-app

# Remove the container:
# docker rm student-app
