import json

import sys
import os
import pytest

lambda_dir = os.path.dirname('/Users/anton_kustikov/my_projects/rsschool_app/product_service/product_service/lambda_func')
sys.path.append(lambda_dir)
from lambda_func import product_by_id


def test_handler_returns_product():
    event = {
        'pathParameters': {
            'productId': '1'
        }
    }
    response = product_by_id.handler(event, None)
    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body['name'] == 'Product 1'
    assert body['price'] == 100

def test_handler_returns_404_for_nonexistent_product():
    event = {
        'pathParameters': {
            'productId': '5'
        }
    }
    response = product_by_id.handler(event, None)
    print(response)
    assert response['statusCode'] == 404
    body = json.loads(response['body'])
    assert body == "'message': 'Product not found'"

if __name__ == '__main__':
    pytest.main()
    