from typing import List, Optional
from app.services.interfaces.vendor_service import IVendorService
from app.repositories.interfaces.vendor_repository import IVendorRepository
from app.domain.schemas.vendor import Vendor, VendorCreate, VendorUpdate
from app.adapters.external_apis.vendor_api_adapter import VendorAPIAdapter
from app.adapters.kafka.kafka_producer import KafkaProducerAdapter
from app.core.config import settings

class VendorService(IVendorService):
    def __init__(
        self,
        vendor_repository: IVendorRepository,
        vendor_api_adapter: VendorAPIAdapter,
        kafka_producer: KafkaProducerAdapter,
    ):
        self.vendor_repository = vendor_repository
        self.vendor_api_adapter = vendor_api_adapter
        self.kafka_producer = kafka_producer

    async def get_vendors(self) -> List[Vendor]:
        vendors = await self.vendor_repository.get_all()
        if not vendors:
            self.kafka_producer.send_message(
                topic=settings.KAFKA_VENDOR_REQUESTS,
                key='vendors',
                message={"vendors": 1},
            )
        return vendors

    async def create_vendor(self, vendor_in: VendorCreate) -> Vendor:
        vendor = await self.vendor_repository.create(vendor_in)
        return vendor

    async def update_vendor(self, vendor_id: str, vendor_in: VendorUpdate) -> Optional[Vendor]:
        vendor = await self.vendor_repository.update(vendor_id, vendor_in)
        return vendor

    async def delete_vendor(self, vendor_id: str) -> bool:
        result = await self.vendor_repository.delete(vendor_id)
        return result
