import boto3
import os

# Use LocalStack endpoint
localstack_url = "http://localhost:4566"

# Create S3 client
s3 = boto3.client('s3', endpoint_url=localstack_url)

# Bucket and file details
bucket_name = "test-bucket"
file_name = "sample.txt"
file_path = os.path.join(os.path.dirname(__file__), file_name)

def create_bucket():
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {e}")

def upload_file():
    try:
        s3.upload_file(file_path, bucket_name, file_name)
        print(f"File '{file_name}' uploaded successfully to bucket '{bucket_name}'.")
    except Exception as e:
        print(f"Error uploading file: {e}")

def list_files():
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print("Bucket is empty.")
    except Exception as e:
        print(f"Error listing files: {e}")

if __name__ == "__main__":
    create_bucket()
    upload_file()
    list_files()
