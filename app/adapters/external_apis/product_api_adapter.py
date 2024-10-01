import aiohttp
from typing import List, Dict
from app.core.config import settings


class ProductAPIAdapter:
    def __init__(self):
        self.all_products_api_url_template = settings.ALL_PRODUCTS_API_URL

    async def fetch_all_products(self, page: int = 1) -> List[Dict]:
        url = self.all_products_api_url_template.format(page=page)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    # Handle error
                    print(f"Error fetching all products: {response.status}")
                    return []