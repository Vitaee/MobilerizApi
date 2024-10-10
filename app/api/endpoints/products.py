from fastapi import APIRouter, Depends, HTTPException, Query
from app.domain.schemas.product import ProductList, Product
from app.services.interfaces.product_service import IProductService
from app.dependencies import get_product_service

router = APIRouter()

@router.get("/", response_model=ProductList)
async def get_products(
    page: int = Query(1, ge=1),
    product_service: IProductService = Depends(get_product_service)
):
    products, pagination = await product_service.get_products(page=page)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return ProductList(data=products, pagination=pagination)