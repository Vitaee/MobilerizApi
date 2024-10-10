from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.domain.models.vendor import Vendor
from app.domain.schemas.vendor import VendorCreate, VendorUpdate
from app.repositories.interfaces.vendor_repository import IVendorRepository


class SQLiteVendorRepository(IVendorRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(self) -> List[Vendor]:
        result = await self.db_session.execute(select(Vendor))
        vendors = result.scalars().all()
        return vendors

    async def create(self, vendor_in: VendorCreate) -> Vendor:
        vendor = Vendor(**vendor_in.model_dump())

        self.db_session.add(vendor)
        await self.db_session.commit()
        await self.db_session.refresh(vendor)
        return vendor

    async def update(self, vendor_id: str, vendor_in: VendorUpdate) -> Optional[Vendor]:
        vendor = await self.get_by_id(vendor_id)
        if vendor:
            for field, value in vendor_in.dict(exclude_unset=True).items():
                setattr(vendor, field, value)
            self.db_session.add(vendor)
            await self.db_session.commit()
            await self.db_session.refresh(vendor)
            return vendor
        return None

    async def delete(self, vendor_id: str) -> bool:
        vendor = await self.get_by_id(vendor_id)
        if vendor:
            await self.db_session.delete(vendor)
            await self.db_session.commit()
            return True
        return False
