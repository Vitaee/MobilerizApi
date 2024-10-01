from typing import Optional, List, Annotated
from pydantic import BaseModel, Field, BeforeValidator
from .pagination import Pagination
from bson import ObjectId 


class VendorBase(BaseModel):
    id: Optional[str] = Field(alias='_id')
    brand_name: str
    brand_logo: str
    class Config:
        json_encoders = {
            ObjectId: str
        }
        arbitrary_types_allowed = True

class VendorCreate(VendorBase):
    pass

class VendorUpdate(BaseModel):
    brand_name: Optional[str]
    brand_logo: Optional[str]

class VendorInDBBase(VendorBase):
    class Config:
        from_attributes = True
        populate_by_name = True

class Vendor(VendorInDBBase):
    products: Optional[List['Product']] = []

class VendorInDB(VendorInDBBase):
    pass

class VendorList(BaseModel):
    data: List[Vendor]
    pagination: Pagination

    class Config:
        from_attributes = True

# Handle forward references
from .product import Product
Vendor.model_rebuild()