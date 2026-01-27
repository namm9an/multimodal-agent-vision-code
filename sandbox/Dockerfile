# Secure Python Sandbox Environment
# Based on slim debian image for minimal attack surface
FROM python:3.11-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # Prevent interactive prompts
    DEBIAN_FRONTEND=noninteractive

# Install only allowed packages
# We use a specific version for reproducibility and security
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    pandas==2.2.0 \
    matplotlib==3.8.2 \
    seaborn==0.13.2 \
    scipy==1.12.0 \
    pillow==10.2.0

# Create a non-root user for execution
# UID 1000 is standard for non-root users
RUN useradd -m -u 1000 sandbox

# Create directories for I/O with restricted permissions
WORKDIR /sandbox
RUN mkdir -p /sandbox/input /sandbox/output && \
    chown -R sandbox:sandbox /sandbox && \
    chmod 700 /sandbox

# Switch to non-root user
USER sandbox

# Set working directory
WORKDIR /sandbox

# Default command (overridden by executor)
CMD ["python3"]
