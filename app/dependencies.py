from app.adapters.external_apis.vendor_api_adapter import VendorAPIAdapter
from app.adapters.external_apis.product_api_adapter import ProductAPIAdapter

from app.services.implementations.product_service_impl import ProductService
from app.services.implementations.vendor_service_impl import VendorService

from app.repositories.implementations.sqlite_product_repository import SQLiteProductRepository
from app.repositories.implementations.sqlite_vendor_repository import SQLiteVendorRepository

from app.adapters.kafka.kafka_producer import  KafkaProducerAdapter
from app.db.session import get_db


async def get_product_service():
    async for db_session in get_db():
        product_repository = SQLiteProductRepository(db_session)
        kafka_producer = KafkaProducerAdapter()
        vendor_api_adapter = VendorAPIAdapter()
        yield ProductService(product_repository, kafka_producer, vendor_api_adapter)


async def get_vendor_service():
    async for db_session in get_db():
        vendor_repository = SQLiteVendorRepository(db_session)
        kafka_producer = KafkaProducerAdapter()
        vendor_api_adapter = VendorAPIAdapter()
        yield  VendorService(vendor_repository, vendor_api_adapter, kafka_producer)