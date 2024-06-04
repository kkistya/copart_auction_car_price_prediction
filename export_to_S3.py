import boto3
import os
from parcer import parce

parce()  # -> to data.csv

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

s3 = boto3.client('s3')

bucket_name = 'k-copart-car-price-prediction'
local_file_path = 'data/data.csv'
s3_file_key = 'data.csv'

try:
    s3.upload_file(local_file_path, bucket_name, s3_file_key)
    print(f'File uploaded to s3://{bucket_name}/{s3_file_key}')
except Exception as e:
    print(f'Error {e}')
