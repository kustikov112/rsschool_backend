import boto3
import uuid
from faker import Faker


dynamodb = boto3.resource('dynamodb')

products_table = dynamodb.Table('products')
stocks_table = dynamodb.Table('stock')

fake = Faker()

def populate_tables(num_items):
    
    for _ in range(num_items):
        product_id = str(uuid.uuid4())
        title = fake.word()
        description = fake.text(max_nb_chars=12)
        price = fake.random_int(min=1, max=1000)

        products_table.put_item(
            Item={
                'id': product_id,
                'title': title,
                'description': description,
                'price': price
            }
        )

        count = fake.random_int(min=1, max=10)

        stocks_table.put_item(
            Item={
                'product_id': product_id,
                'count': count
            }
        )
populate_tables(5)
