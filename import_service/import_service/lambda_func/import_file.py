import os
import json
import boto3

s3 = boto3.client('s3')

def handler(event, context):
    file_name = event['queryStringParameters']['name']
    bucket_name = os.environ['BUCKET_NAME']
    # bucket_name = 'task-5-bucket-for-shop-csv'

    key = f"uploaded/{file_name}"
    
    params = {
        'Bucket': bucket_name,
        'Key': key,
    }
    
    signed_url = s3.generate_presigned_url('put_object', Params=params)
    # return signed_url
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
            "content-type":"*/*"
        },
        'body': signed_url
    }

# print(handler(True, True))
