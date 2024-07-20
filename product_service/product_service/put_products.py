from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class PutProducts(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.put_products = _lambda.Function(
            self, 'CreateProductHandler',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='put_product.handler',
            code=_lambda.Code.from_asset('product_service/lambda_func/'),
            environment=environment
        )
