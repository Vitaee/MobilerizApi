from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.schemas.vendor import Vendor, VendorCreate, VendorUpdate


class IVendorService(ABC):
    @abstractmethod
    async def get_vendor(self, vendor_id: str) -> Optional[Vendor]:
        pass

    @abstractmethod
    async def get_vendors(self) -> List[Vendor]:
        pass

    @abstractmethod
    async def create_vendor(self, vendor_in: VendorCreate) -> Vendor:
        pass

    @abstractmethod
    async def update_vendor(self, vendor_id: str, vendor_in: VendorUpdate) -> Optional[Vendor]:
        pass

    @abstractmethod
    async def delete_vendor(self, vendor_id: str) -> bool:
        pass
