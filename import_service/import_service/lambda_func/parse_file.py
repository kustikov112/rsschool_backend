import os
import boto3
import csv
import io
import json

s3 = boto3.client('s3')
sqs = boto3.client('sqs')


def handler(event, context):
    bucket_name = 'task-5-bucket-for-shop-csv'
    # bucket_name = os.environ['BUCKET_NAME']

    response = sqs.get_queue_url(QueueName='catalogItemsQueue')
    queue_url = response['QueueUrl']
    
    for record in event['Records']:
        key = record['s3']['object']['key']
        
        response = s3.get_object(Bucket=bucket_name, Key=key)
        body = response['Body']
        
        csv_file = io.StringIO(body.read().decode('utf-8'))
        reader = csv.DictReader(csv_file)
        for row in reader:
            print(row)
            sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(row)
            )        
        copy_source = {'Bucket': bucket_name, 'Key': key}
        parsed_key = key.replace('uploaded/', 'parsed/')
        s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=parsed_key)
        
        # print(key)

        if key != 'uploaded/':
            s3.delete_object(Bucket=bucket_name, Key=key)