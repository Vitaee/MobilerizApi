from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.schemas.vendor import Vendor
from app.services.interfaces.vendor_service import IVendorService
from app.dependencies import get_vendor_service

router = APIRouter()

@router.get("/", response_model=List[Vendor])
async def get_vendors(vendor_service: IVendorService = Depends(get_vendor_service)):
    vendors = await vendor_service.get_vendors()
    if not vendors:
        raise HTTPException(status_code=404, detail="No vendors found")
    return vendors
