import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.core.schemas import Product, ProductResponse

class ProductService:
    def __init__(self):
        self.api_url = settings.PRODUCT_API_URL

    async def get_products(self, brand_id: str, page: int = 1):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/product/brand/{brand_id}/?page={page}")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch products")

        data = response.json()
        
        products = [
            Product(
                id=item["_id"],
                name=item["product_name"],
                description=item["product_description"],
                price=float(item["product_price"].replace(" TL", "")),
                photoUrl=item["product_image"][0] if item["product_image"] else "",
                category=item["product_category"]
            )
            for item in data["data"]
        ]

        return ProductResponse(
            success=data["success"],
            data=products,
            pagination=data["pagination"]
        )

    async def get_product(self, product_id: str):
        # Implement get single product logic here
        # This might require a separate API call or filtering from the list
        pass