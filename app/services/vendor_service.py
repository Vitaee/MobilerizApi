import httpx
from fastapi import HTTPException
from app.core.config import settings
from app.core.schemas import Vendor, VendorResponse

class VendorService:
    def __init__(self):
        self.api_url = settings.VENDOR_API_URL

    async def get_vendors(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.api_url}/brand/")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch vendors")

        data = response.json()
        
        vendors = [
            Vendor(
                _id=item["_id"],
                brand_name=item["brand_name"],
                brand_logo=item["brand_logo"],
                createdAt=item["createdAt"],
                updatedAt=item["updatedAt"]
            )
            for item in data["data"]
        ]

        return VendorResponse(
            success=data["success"],
            data=vendors,
            pagination=data.get("pagination", {})  # Add pagination if it exists in the response
        )

    async def get_vendor(self, vendor_id: str):
        # Implement get single vendor logic here
        # This might require a separate API call or filtering from the list
        pass