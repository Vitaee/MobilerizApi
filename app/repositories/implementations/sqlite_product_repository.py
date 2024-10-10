from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import func
from app.domain.models.product import Product
from app.domain.schemas.product import ProductCreate, ProductUpdate
from app.repositories.interfaces.product_repository import IProductRepository
from app.domain.schemas.pagination import Pagination


class SQLiteProductRepository(IProductRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_all(self, page: int = 1, per_page: int = 10) -> Tuple[List[Product], Pagination]:
        offset = (page - 1) * per_page
        total = await self.db_session.execute(select(func.count(Product.id)))
        total_count = total.scalar()
        result = await self.db_session.execute(
            select(Product).offset(offset).limit(per_page)
        )
        products = result.scalars().all()
        number_of_page = (total_count + per_page - 1) // per_page
        pagination = Pagination(
            page_number=page,
            per_page=per_page,
            number_of_data=total_count,
            number_of_page=number_of_page,
        )
        return products, pagination

    async def create(self, product_in: ProductCreate) -> Product:
        print(product_in.model_dump())
        product = Product(**product_in.model_dump())
        self.db_session.add(product)
        await self.db_session.commit()
        await self.db_session.refresh(product)
        return product

    async def update(self, product_id: str, product_in: ProductUpdate) -> Optional[Product]:
        product = await self.get_by_id(product_id)
        if product:
            for field, value in product_in.dict(exclude_unset=True).items():
                setattr(product, field, value)
            self.db_session.add(product)
            await self.db_session.commit()
            await self.db_session.refresh(product)
            return product
        return None

    async def delete(self, product_id: str) -> bool:
        product = await self.get_by_id(product_id)
        if product:
            await self.db_session.delete(product)
            await self.db_session.commit()
            return True
        return False