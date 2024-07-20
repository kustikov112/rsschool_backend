from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Stack
)
import dotenv
import os


from constructs import Construct

class AuthorizationServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        dotenv.load_dotenv()
        login = 'kustikov'
        SECRET_KEY = os.getenv(login)

        _lambda.Function(
            self, 'BasicAuthorizerLambda',
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler='basic_authorizer.handler',
            code=_lambda.Code.from_asset('lambda/'),
            environment={
                login: SECRET_KEY
            },
            function_name='AuthFunction'
        )
