import os
import boto3
import json
import uuid



def handler(event, context):
    try:
        dynamodb = boto3.client('dynamodb', 'eu-central-1')

        count_table_name = 'stock'
        product_table_name = 'products'

        event = json.loads(event['body'])

        required_fields = ['title', 'description', 'price', 'count']
        for field in required_fields:
            if field not in event:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': f'{field} is required'})
                }

        product_id = str(uuid.uuid4())

        new_product = {
            'id': {'S': product_id},
            'title': {'S': event['title']},
            'description': {'S': event['description']},
            'price': {'N': str(event['price'])}
        }

        new_count = {
            'product_id': {'S': product_id},
            'count': {'N': str(event['count'])}
        }

        try:
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
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }

        return {
            'statusCode': 201,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
                "content-type":"application/json",
                "Access-Control-Allow-Headers": "*"
                },
            'body': json.dumps({
                'id': product_id,
                'title': event['title'],
                'description': event['description'],
                'price': event['price'],
                'count': event['count']
            })
        }
    except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }


# print(handler({"count":2,"price":2,"description":"ssssetw","title":"weaaast"}, True))