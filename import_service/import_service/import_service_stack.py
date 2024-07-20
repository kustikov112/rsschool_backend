from aws_cdk import Stack
from import_service.api_gateway import ApiGateway
from import_service.import_products_lambda import ImportServiceLambda
from import_service.parse_products_lambda import ParseFileLambda
from constructs import Construct


class ImportServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = 'task-5-bucket-for-shop-csv'

        import_products_lambda = ImportServiceLambda(self, 'ImportLambda', bucket_name)
        ParseFileLambda(self, 'ParseLambda', bucket_name)
        ApiGateway(self, 'APIGateway',
                    import_products_fn=import_products_lambda.import_products_file,
                    )


