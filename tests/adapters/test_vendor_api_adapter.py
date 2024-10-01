import asyncio
from app.adapters.external_apis.vendor_api_adapter import VendorAPIAdapter

async def test_fetch_vendors():
    adapter = VendorAPIAdapter()
    vendors = await adapter.fetch_vendors()
    assert isinstance(vendors, list)
    assert len(vendors) > 0

async def test_fetch_products_by_vendor():
    adapter = VendorAPIAdapter()
    vendor_id = "6681fee311f417006b8096a7"  # Example vendor ID
    products = await adapter.fetch_products_by_vendor(vendor_id)
    assert isinstance(products, list)
    assert len(products) > 0

if __name__ == "__main__":
    asyncio.run(test_fetch_vendors())
    asyncio.run(test_fetch_products_by_vendor())