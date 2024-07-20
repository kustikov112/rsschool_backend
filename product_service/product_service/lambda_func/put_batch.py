import json
import boto3
import os
import uuid


dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')

def handler(event, context):
    products_for_sns = []
    for record in event['Records']:
        record = json.loads(record['body'])
        dynamodb = boto3.client('dynamodb', 'eu-central-1')
        # topic = sns_client.create_topic(Name='createProductTopic')
        sns_topic_arn = os.environ['SNS_TOPIC_ARN']
        count_table_name = 'stock'
        product_table_name = 'products'
    
        required_fields = ['title', 'description', 'price', 'count']
        for field in required_fields:
            if field not in record:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'{field} is required'})
                }
        product_id = str(uuid.uuid4())
        new_product = {
            'id': {'S': product_id},
            'title': {'S': record['title']},
            'description': {'S': record['description']},
            'price': {'N': str(record['price'])}
        }

        new_count = {
            'product_id': {'S': product_id},
            'count': {'N': str(record['count'])}
        }
        
        sns_product = {
            'id': product_id,
            'title': record['title'],
            'description': record['description'],
            'price': record['price'],
            'count': record['count']
        }
        products_for_sns.append(sns_product)

        dynamodb.transact_write_items(
                TransactItems=[
                    {
                        'Put': {
                            'TableName': product_table_name,
                            'Item': new_product
                        }
                    },
                    {
                        'Put': {
                            'TableName': count_table_name,
                            'Item': new_count
                        }
                    }
                ]
            )
    sns_message = {
        'default': json.dumps({
            'message': 'Products created successfully',
            'products': products_for_sns
        })
    }

    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(sns_message),
        MessageStructure='json'
    )
    print(f"Message sent to SNS topic: {response['MessageId']}")

    return {
        'headers': {
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
        },
        'statusCode': 200,
        'body': json.dumps('Batch processed successfully')
    }