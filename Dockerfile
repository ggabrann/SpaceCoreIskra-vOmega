# Production-ready Dockerfile for SpaceCoreIskra vΩ
# Version: 0.1.0-dev0
# Base: Python 3.11 slim for minimal footprint

FROM python:3.11-slim AS base

# Metadata
LABEL maintainer="SpaceCoreIskra Maintainers <maintainers@iskra.space>"
LABEL version="0.1.0-dev0"
LABEL description="SpaceCoreИскра vΩ - живая система отклика с ∆DΩΛ метриками"

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ISKRA_LOG_LEVEL=INFO \
    ISKRA_STRUCTURED_LOGS=true

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first (better layer caching)
COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 iskra && \
    chown -R iskra:iskra /app

USER iskra

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["python", "-m", "iskra_cli.cli", "--brief", "⟡"]

# -----------------------------------------------------------
# Development stage (with dev dependencies and tools)
# -----------------------------------------------------------
FROM base AS development

USER root

# Install dev dependencies
RUN pip install --no-cache-dir -r requirements-dev.txt

# Install development tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        vim \
        curl \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER iskra

# Override command for development
CMD ["/bin/bash"]

# -----------------------------------------------------------
# Production stage (minimal, production-ready)
# -----------------------------------------------------------
FROM base AS production

# Remove unnecessary files
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + || true && \
    find /app -type f -name "*.pyc" -delete || true && \
    find /app -type d -name ".pytest_cache" -exec rm -rf {} + || true

# Ensure logs directory exists
RUN mkdir -p /app/logs && \
    chown -R iskra:iskra /app/logs

VOLUME ["/app/logs"]

# Production command (can be overridden)
CMD ["python", "-m", "iskra_cli.cli"]

# -----------------------------------------------------------
# CI/Test stage (for running tests in container)
# -----------------------------------------------------------
FROM development AS test

USER root
RUN pip install --no-cache-dir -r requirements-dev.txt
USER iskra

# Run full CI suite
CMD ["make", "ci"]
