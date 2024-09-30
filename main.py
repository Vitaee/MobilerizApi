from fastapi import FastAPI, HTTPException

app = FastAPI()

# Sample product data
products = [
    {
        "id": "1",
        "name": "Product A",
        "description": "Description of Product A",
        "price": 29.99,
        "photoUrl": "https://xelltechnology.com/wp-content/uploads/2022/04/dummy6.jpg",
        "category": "Category A"
    },
    {
        "id": "2",
        "name": "Product B",
        "description": "Description of Product B",
        "price": 49.99,
        "photoUrl": "https://xelltechnology.com/wp-content/uploads/2022/04/dummy3.jpg",
        "category": "Category B"
    }
]

@app.get("/products")
async def get_products():
    return products

@app.get("/products/{product_id}")
async def get_product(product_id: str):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
