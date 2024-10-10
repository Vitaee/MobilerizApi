from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.schemas.vendor import VendorCreate, VendorUpdate
from app.domain.models.vendor import Vendor


class IVendorRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Vendor]:
        pass

    @abstractmethod
    async def create(self, vendor_in: VendorCreate) -> Vendor:
        pass

    @abstractmethod
    async def update(self, vendor_id: str, vendor_in: VendorUpdate) -> Optional[Vendor]:
        pass

    @abstractmethod
    async def delete(self, vendor_id: str) -> bool:
        pass