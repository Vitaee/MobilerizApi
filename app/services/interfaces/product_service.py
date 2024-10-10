from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.schemas.product import Product, ProductCreate, ProductUpdate
from app.domain.schemas.pagination import Pagination


class IProductService(ABC):
    @abstractmethod
    async def get_products(self, page: int = 1) -> Tuple[List[Product], Pagination]:
        pass

    @abstractmethod
    async def create_product(self, product_in: ProductCreate) -> Product:
        pass

    @abstractmethod
    async def update_product(self, product_id: str, product_in: ProductUpdate) -> Optional[Product]:
        pass

    @abstractmethod
    async def delete_product(self, product_id: str) -> bool:
        pass

    @abstractmethod
    async def request_product_from_kafka(self, product_id: str):
        pass
