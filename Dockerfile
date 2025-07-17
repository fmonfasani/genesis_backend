# Genesis Backend - Multi-stage Docker build
# Production-ready container for Genesis Backend

# Build stage
FROM python:3.11-slim as builder

LABEL maintainer="Genesis Engine Team <team@genesis-engine.dev>"
LABEL org.opencontainers.image.title="Genesis Backend"
LABEL org.opencontainers.image.description="Backend Code Generation Agents for Genesis Engine"
LABEL org.opencontainers.image.source="https://github.com/genesis-engine/genesis-backend"
LABEL org.opencontainers.image.version="1.0.0"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements first for better caching
COPY pyproject.toml README.md ./
COPY src/ ./src/

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

# Development stage
FROM builder as development

# Install development dependencies
RUN pip install -e ".[dev,test]"

# Set working directory
WORKDIR /app

# Copy source code
COPY . .

# Create non-root user for development
RUN useradd --create-home --shell /bin/bash genesis && \
    chown -R genesis:genesis /app
USER genesis

# Default command for development
CMD ["python", "-m", "genesis_backend"]

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash --uid 1000 genesis

# Create application directory
WORKDIR /app

# Copy application code
COPY --chown=genesis:genesis src/ ./src/
COPY --chown=genesis:genesis examples/ ./examples/
COPY --chown=genesis:genesis README.md ./

# Switch to non-root user
USER genesis

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import genesis_backend; print('Genesis Backend is healthy')" || exit 1

# Expose port (if needed for future web interface)
EXPOSE 8000

# Default command
CMD ["python", "-c", "import genesis_backend; print('Genesis Backend container started successfully')"]

# Testing stage
FROM development as testing

# Install testing dependencies
RUN pip install pytest-cov pytest-mock pytest-asyncio

# Copy test files
COPY tests/ ./tests/

# Run tests by default
CMD ["pytest", "tests/", "-v", "--cov=genesis_backend"]

# Documentation stage
FROM python:3.11-slim as docs

# Install documentation dependencies
RUN pip install mkdocs mkdocs-material

# Copy documentation
COPY docs/ ./docs/
COPY README.md CHANGELOG.md ./

# Generate documentation
RUN mkdocs build

# Serve documentation
EXPOSE 8080
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8080"]

# Example usage stage
FROM production as examples

# Set working directory to examples
WORKDIR /app/examples

# Default command runs examples
CMD ["python", "basic_usage.py"]

# Minimal stage for CI/CD
FROM python:3.11-alpine as minimal

# Install minimal dependencies
RUN apk add --no-cache git curl

# Copy only necessary files
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create minimal user
RUN adduser -D -s /bin/sh genesis

# Switch to non-root user
USER genesis

# Working directory
WORKDIR /app

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=5s --retries=2 \
    CMD python -c "import genesis_backend" || exit 1

# Default command
CMD ["python", "-c", "import genesis_backend; print('Genesis Backend minimal container ready')"]
