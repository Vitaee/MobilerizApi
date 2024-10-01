import aiohttp
from typing import List, Dict
from app.core.config import settings


class VendorAPIAdapter:
    def __init__(self):
        self.vendor_api_url = settings.VENDOR_API_URL
        self.products_api_url_template = settings.PRODUCTS_API_URL_TEMPLATE
        self.all_products_api_url = settings.ALL_PRODUCTS_API_URL
    
    async def fetch_vendors(self) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.vendor_api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    # Handle error
                    print(f"Error fetching vendors: {response.status}")
                    return []
    
    async def fetch_products_by_vendor(self, vendor_id: str, page: int = 1) -> List[Dict]:
        url = self.products_api_url_template.format(brand_id=vendor_id, page=page)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    # Handle error
                    print(f"Error fetching products for vendor {vendor_id}: {response.status}")
                    return []
                
    async def fetch_all_products(self, page: int = 1):
        url = self.all_products_api_url.format(page=page)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                else:
                    # Handle error
                    print(f"Error fetching ALL products from vendor api: {response.status}")
                    return []