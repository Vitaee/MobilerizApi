from typing import List, Optional
from app.services.interfaces.vendor_service import IVendorService
from app.repositories.interfaces.vendor_repository import IVendorRepository
from app.domain.schemas.vendor import Vendor, VendorCreate, VendorUpdate
from app.adapters.external_apis.vendor_api_adapter import VendorAPIAdapter


class VendorService(IVendorService):
    def __init__(
        self,
        vendor_repository: IVendorRepository,
        vendor_api_adapter: VendorAPIAdapter,
    ):
        self.vendor_repository = vendor_repository
        self.vendor_api_adapter = vendor_api_adapter

    async def get_vendor(self, vendor_id: str) -> Optional[Vendor]:
        vendor = await self.vendor_repository.get_by_id(vendor_id)
        if not vendor:
            # Fetch vendor from external API
            vendors_data = await self.vendor_api_adapter.fetch_vendors()
            for vendor_data in vendors_data:
                vendor_in = VendorCreate(
                    id=vendor_data['_id'],
                    brand_name=vendor_data['brand_name'],
                    brand_logo=vendor_data['brand_logo'],
                )

                print(vendor_in)

                print('^^^^^^^^^ VENDOR IN ^^^^^^^^^^')
                await self.vendor_repository.create(vendor_in)
            vendor = await self.vendor_repository.get_by_id(vendor_id)
        return vendor

    async def get_vendors(self) -> List[Vendor]:
        vendors = await self.vendor_repository.get_all()
        if not vendors:
            # Fetch vendors from external API
            vendors_data = await self.vendor_api_adapter.fetch_vendors()
            for vendor_data in vendors_data:
                vendor_in = VendorCreate(
                    _id=vendor_data['_id'],
                    brand_name=vendor_data['brand_name'],
                    brand_logo=vendor_data['brand_logo'],
                )
                await self.vendor_repository.create(vendor_in)
            vendors = await self.vendor_repository.get_all()
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
