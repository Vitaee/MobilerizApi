from typing import List, Optional, Tuple
from app.services.interfaces.product_service import IProductService
from app.repositories.interfaces.product_repository import IProductRepository
from app.adapters.kafka.kafka_producer import KafkaProducerAdapter
from app.adapters.external_apis.vendor_api_adapter import VendorAPIAdapter
from app.domain.schemas.product import Product, ProductCreate, ProductUpdate
from app.domain.schemas.pagination import Pagination
from app.core.config import settings


class ProductService(IProductService):
    def __init__(
        self,
        product_repository: IProductRepository,
        kafka_producer: KafkaProducerAdapter,
        vendor_api_adapter: VendorAPIAdapter,
    ):
        self.product_repository = product_repository
        self.kafka_producer = kafka_producer
        self.vendor_api_adapter = vendor_api_adapter

    async def get_product(self, product_id: str) -> Optional[Product]:
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            # Send a message to Kafka to fetch the product via Flink
            self.kafka_producer.send_message(
                topic=settings.KAFKA_PRODUCT_REQ_BY_ID,
                key=product_id,
                message={"product_id": product_id},
            )
            return None
        return product

    async def get_products(self, page: int = 1) -> Tuple[List[Product], Pagination]:
        products, pagination = await self.product_repository.get_all(page=page)
        if not products:
            # Fetch products from external API
            products_data = await self.vendor_api_adapter.fetch_all_products(page=page)
            # Process and save products
            for product_data in products_data:
                product_in = ProductCreate(
                    _id=product_data['_id'],
                    product_name=product_data['product_name'],
                    product_description=product_data['product_description'],
                    product_price=float(product_data['product_price'].replace('₺', '').replace(',', '.')),
                    product_image=str(product_data['product_image'][0]),
                    product_category=product_data['product_category'],
                    product_brand_id=product_data['product_brand_id']
                )
                await self.product_repository.create(product_in)
            products, pagination = await self.product_repository.get_all(page=page)
        return products, pagination

    async def create_product(self, product_in: ProductCreate) -> Product:
        product = await self.product_repository.create(product_in)
        return product

    async def update_product(self, product_id: str, product_in: ProductUpdate) -> Optional[Product]:
        product = await self.product_repository.update(product_id, product_in)
        return product

    async def delete_product(self, product_id: str) -> bool:
        result = await self.product_repository.delete(product_id)
        return result

    async def request_product_from_kafka(self, product_id: str):
        # Send a message to Kafka to fetch the product via Flink
        self.kafka_producer.send_message(
            topic=settings.KAFKA_PRODUCT_REQ_BY_ID,
            key=product_id,
            message={"product_id": product_id},
        )