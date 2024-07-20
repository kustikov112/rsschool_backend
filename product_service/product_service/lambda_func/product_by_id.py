import json
import os
import boto3


    
def handler(event, context):

    try: 
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))

        count_table_name = os.getenv('STOCK_TABLE_NAME')
        product_table_name = os.getenv('PRODUCTS_TABLE_NAME')

        count_table = dynamodb.Table(count_table_name)
        product_table = dynamodb.Table(product_table_name)

        product_id = event['pathParameters']['productId']

        count_response = count_table.get_item(Key={'product_id': product_id})
        count_item = count_response.get('Item')
        if not count_item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Product count not found'})
            }

        product_response = product_table.get_item(Key={'id': product_id})
        product_item = product_response.get('Item')
        if not product_item:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Product details not found'})
            }
        
        result = {
            'id': product_id,
            'count': str(count_item.get('count')),
            'title': product_item.get('title'),
            'description': product_item.get('description'),
            'price': str(product_item.get('price'))
        }

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
                "content-type":"application/json"
            },
            'body': json.dumps(result)
        }
    except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
                                    