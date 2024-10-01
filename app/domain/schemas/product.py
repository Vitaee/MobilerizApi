from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.networks import AnyUrl
from .pagination import Pagination


class ProductBase(BaseModel):
    id: str = Field(..., alias='_id')
    name: str = Field(..., alias='product_name')
    description: str = Field(..., alias='product_description')
    price: str = Field(..., alias='product_price')
    photo_url: AnyUrl = Field(..., alias='product_image')
    category: str = Field(..., alias='product_category')
    vendor_id: Optional[str] = Field(None, alias='product_brand_id')

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[str]
    photo_url: Optional[AnyUrl]
    category: Optional[str]
    vendor_id: Optional[str]

class ProductInDBBase(ProductBase):
    class Config:
        from_attributes = True
        populate_by_name = True

class Product(ProductInDBBase):
    vendor: Optional['Vendor'] = None  # Forward reference

class ProductInDB(ProductInDBBase):
    pass

class ProductList(BaseModel):
    data: List[Product]
    pagination: Pagination

    class Config:
        from_attributes = True

# Handle forward references
from .vendor import Vendor
Product.model_rebuild()