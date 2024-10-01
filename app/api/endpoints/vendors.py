from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.domain.schemas.vendor import Vendor
from app.services.interfaces.vendor_service import IVendorService
from app.dependencies import get_vendor_service

router = APIRouter()

@router.get("/", response_model=List[Vendor])
async def get_vendors(vendor_service: IVendorService = Depends(get_vendor_service)):
    vendors = await vendor_service.get_vendors()
    print(vendors)
    print('^^^^^^^^^^^^^^^^^^^^^^^^')
    if not vendors:
        raise HTTPException(status_code=404, detail="No vendors found")
    return vendors

@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor(vendor_id: str, vendor_service: IVendorService = Depends(get_vendor_service)):
    vendor = await vendor_service.get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor