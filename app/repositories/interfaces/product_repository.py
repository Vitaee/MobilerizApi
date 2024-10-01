from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from app.domain.schemas.product import ProductCreate, ProductUpdate
from app.domain.models.product import Product
from app.domain.schemas.pagination import Pagination


class IProductRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[Product]:
        pass

    @abstractmethod
    async def get_all(self, page: int = 1, per_page: int = 10) -> Tuple[List[Product], Pagination]:
        pass

    @abstractmethod
    async def create(self, product_in: ProductCreate) -> Product:
        pass

    @abstractmethod
    async def update(self, product_id: str, product_in: ProductUpdate) -> Optional[Product]:
        pass

    @abstractmethod
    async def delete(self, product_id: str) -> bool:
        pass