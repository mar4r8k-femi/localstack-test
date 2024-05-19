FROM gitpod/workspace-full

# Specify the Python version
RUN pyenv install 3.8.10
RUN pyenv global 3.8.10

# Install dependencies
RUN pip install boto3 localstack awscli

# Ensure LocalStack services are up and running
RUN mkdir -p /etc/localstack
RUN echo 'SERVICES=s3,lambda,dynamodb,sqs' > /etc/localstack/localstack.conf
