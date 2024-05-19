import boto3
import os
import time

# Set the LocalStack endpoint URL
localstack_url = "http://localhost:4566"

# Create a new S3 client using Boto3
s3_client = boto3.client(
    's3',
    endpoint_url=localstack_url,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Create a new DynamoDB client using Boto3
dynamodb_client = boto3.client(
    'dynamodb',
    endpoint_url=localstack_url,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# Create a new SQS client using Boto3
sqs_client = boto3.client(
    'sqs',
    endpoint_url=localstack_url,
    aws_access_key_id='test',
    aws_secret_access_key='test',
    region_name='us-east-1'
)

# S3 operations
bucket_name = 'my-localstack-bucket'
s3_client.create_bucket(Bucket=bucket_name)
print(f'Created S3 bucket: {bucket_name}')

file_name = 'sample.txt'
with open(file_name, 'w') as f:
    f.write('Hello, LocalStack!')

s3_client.upload_file(file_name, bucket_name, file_name)
print(f'Uploaded {file_name} to {bucket_name}')

response = s3_client.list_objects_v2(Bucket=bucket_name)
print('Objects in S3 bucket:')
for obj in response.get('Contents', []):
    print(f'- {obj["Key"]}')

# DynamoDB operations
table_name = 'my-localstack-table'
dynamodb_client.create_table(
    TableName=table_name,
    KeySchema=[
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)
print(f'Created DynamoDB table: {table_name}')

# Wait for the table to become active
time.sleep(5)

dynamodb_client.put_item(
    TableName=table_name,
    Item={
        'id': {'S': '123'},
        'message': {'S': 'Hello, DynamoDB!'}
    }
)
print(f'Inserted item into DynamoDB table: {table_name}')

response = dynamodb_client.scan(TableName=table_name)
print('Items in DynamoDB table:')
for item in response.get('Items', []):
    print(f'- {item["id"]["S"]}: {item["message"]["S"]}')

# SQS operations
queue_name = 'my-localstack-queue'
response = sqs_client.create_queue(QueueName=queue_name)
queue_url = response['QueueUrl']
print(f'Created SQS queue: {queue_name}')

sqs_client.send_message(QueueUrl=queue_url, MessageBody='Hello, SQS!')
print(f'Sent message to SQS queue: {queue_name}')

response = sqs_client.receive_message(QueueUrl=queue_url)
print('Messages in SQS queue:')
for message in response.get('Messages', []):
    print(f'- {message["Body"]}')

# Clean up: Delete the file, S3 bucket, DynamoDB table, and SQS queue
os.remove(file_name)
s3_client.delete_object(Bucket=bucket_name, Key=file_name)
s3_client.delete_bucket(Bucket=bucket_name)
print(f'Deleted {file_name} and S3 bucket: {bucket_name}')

dynamodb_client.delete_table(TableName=table_name)
print(f'Deleted DynamoDB table: {table_name}')

sqs_client.delete_queue(QueueUrl=queue_url)
print(f'Deleted SQS queue: {queue_name}')
