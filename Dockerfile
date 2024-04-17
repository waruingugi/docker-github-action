# Pull official base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

# Create a user to avoid running containers as root in production
RUN addgroup --system admin \
    && adduser --system --ingroup admin admin

# Install os-level dependencies (as root)
RUN apt-get update && apt-get install -y -q --no-install-recommends \
    # dependencies for building Python packages
    build-essential \
    # postgres client (psycopyg2) dependencies
    build-essential \
    libpq-dev \
    # cleaning up unused fiels to reduce the image size
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Switch to the non root user
USER admin

# Create a directory for the source code and use it as the base path
WORKDIR /home/app

# Copy the python dependencies list for pip
COPY --chown=admin:admin ./requirements.txt .

# Switch to the root user temporary, to grant execution permission
USER root

# Install python packages at system level
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script which waits for the db to be ready
COPY --chown=admin:admin /scripts/entrypoint.sh /scripts/entrypoint.sh

# Copy script that tests the server
COPY --chown=admin:admin /scripts/test.sh /scripts/test.sh

# Grant execution permissions on the files
RUN chmod +x /scripts/entrypoint.sh && \
    chmod +x /scripts/test.sh

# Switch back to non-root user
USER admin

# This script will run before any command is executed on the container
ENTRYPOINT [ "/scripts/entrypoint.sh" ]

COPY . .
