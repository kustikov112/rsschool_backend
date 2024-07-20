from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_lambda_event_sources as lambda_event_sources,
)
from constructs import Construct


class PutBatchProcessor(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SNS imlementation
        create_product_topic = sns.Topic(
            self, 'CreateProductTopic',
            topic_name='createProductTopic'
        )

        create_product_topic.add_subscription(
            subscriptions.EmailSubscription('antony01904@gmail.com')
        )

        # SQS implementatoin
        catalog_items_queue = sqs.Queue(self, "CatalogItemsQueue",
                                        queue_name="catalogItemsQueue"
                                        )
        event_source = lambda_event_sources.SqsEventSource(catalog_items_queue,
            batch_size=5  
        )
        environment['SNS_TOPIC_ARN'] = create_product_topic.topic_arn
        self.put_batch = _lambda.Function(
            self, 'PutBatch',
            runtime=_lambda.Runtime.PYTHON_3_11,
            code=_lambda.Code.from_asset('product_service/lambda_func/'),
            handler='put_batch.handler',
            environment=environment
        )


        #SQS policy
        self.put_batch.add_event_source(event_source)
        catalog_items_queue.grant_consume_messages(self.put_batch)
        # SNS POlicy
        create_product_topic.grant_publish(self.put_batch)
