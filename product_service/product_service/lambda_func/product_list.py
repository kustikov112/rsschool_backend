import json
import os
import boto3


def handler(event, context):
    
    # try: 
    dynamodb = boto3.resource('dynamodb', 'eu-central-1')
    
    count_table_name = 'stock' #os.getenv('STOCK_TABLE_NAME')
    product_table_name = 'products' #os.getenv('PRODUCTS_TABLE_NAME')

    count_table = dynamodb.Table(count_table_name)
    product_table = dynamodb.Table(product_table_name)

    count_response = count_table.scan()
    count_items = count_response.get('Items', [])

    product_response = product_table.scan()
    product_items = product_response.get('Items', [])


    product_dict = {item['id']: item for item in product_items}

    for count_item in count_items:
        product_id = count_item['product_id']
        if product_id in product_dict:
            product_dict[product_id]['count'] = str(count_item['count'])
            product_dict[product_id]['price'] = str(product_dict[product_id]['price'])
        else:
            product_dict[product_id] = {
                'id': product_id,
                'count': count_item['count']
            }

    products = list(product_dict.values())
    # print(f'This is products: {product_dict}')


    return {'statusCode': 200,
            'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": 'GET, POST, PUT, DELETE, OPTIONS',
            "content-type":"application/json"
            },
            "body": json.dumps(products)
    }

                                   