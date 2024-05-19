FROM gitpod/workspace-full:latest

# Install LocalStack dependencies
RUN apt-get update && apt-get install -y python3-pip python3-dev
RUN pip install localstack awscli-local

# Install project dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project files
COPY . /workspace

# Set environment variables for LocalStack
ENV EDGE_PORT=4566
ENV SERVICES=s3,lambda,dynamodb

# Expose LocalStack port
EXPOSE 4566
