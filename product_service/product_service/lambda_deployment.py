from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb
from product_service.api_gateway import ApiGateway
from product_service.get_product_by_id import ProductsById
from product_service.get_products import GetProducts
from product_service.put_products import PutProducts
from product_service.put_batch_in_dynamo import PutBatchProcessor
from constructs import Construct


class MyCdkAppStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        products_table_name = 'products'
        stock_table_name = 'stock'


        products_table = dynamodb.Table.from_table_name(self, 'ProductsTable', products_table_name)
        stock_table = dynamodb.Table.from_table_name(self, 'StockTable', stock_table_name)

        environment = {
            "PRODUCTS_TABLE_NAME": stock_table_name,
            "STOCK_TABLE_NAME": stock_table_name,
        }

        get_products_list_lbd = GetProducts(self, 'ProductsList', environment)
        get_product_by_id_lbd = ProductsById(self, 'ProductsByID', environment)
        put_products_lbd = PutProducts(self, 'PutProducts', environment)
        put_batch_processor_lbd = PutBatchProcessor(self, 'PutBatchProcessor', environment)
        ApiGateway(self, 'APIGateway',
                    get_products_list_fn=get_products_list_lbd.get_products_list,
                    get_products_by_id_fn=get_product_by_id_lbd.get_products_by_id,
                    put_products_fn=put_products_lbd.put_products)


        products_table.grant_read_write_data(get_products_list_lbd.get_products_list)
        stock_table.grant_read_write_data(get_products_list_lbd.get_products_list)
        products_table.grant_read_write_data(get_product_by_id_lbd.get_products_by_id)
        stock_table.grant_read_write_data(get_product_by_id_lbd.get_products_by_id)
        products_table.grant_read_write_data(put_products_lbd.put_products)
        stock_table.grant_read_write_data(put_products_lbd.put_products)
        products_table.grant_read_write_data(put_batch_processor_lbd.put_batch)
        stock_table.grant_read_write_data(put_batch_processor_lbd.put_batch)
