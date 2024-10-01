from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from pydantic.networks import AnyUrl
from .pagination import Pagination
from bson import ObjectId


class ProductBase(BaseModel):
    id: str = Field(..., alias='_id')
    name: str = Field(..., alias='product_name')
    description: str = Field(..., alias='product_description')
    price: float = Field(..., alias='product_price')
    photo_url: str = Field(..., alias='product_image')
    category: str = Field(..., alias='product_category')
    vendor_id: Optional[str] = Field(None, alias='product_brand_id')

    @field_validator('photo_url')
    def convert_photo_url_to_str(cls, v):
        return str(v)
    
    class Config:
        json_encoders = {
            ObjectId: str,
        }
        arbitrary_types_allowed = True

    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[str]
    photo_url: Optional[str]
    category: Optional[str]
    vendor_id: Optional[str]

class ProductInDBBase(ProductBase):
    class Config:
        from_attributes = True
        populate_by_name = True

class Product(ProductInDBBase):
    pass

class ProductInDB(ProductInDBBase):
    pass

class ProductList(BaseModel):
    data: List[Product]
    pagination: Pagination

    class Config:
        from_attributes = True
