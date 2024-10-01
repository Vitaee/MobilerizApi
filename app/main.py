from fastapi import FastAPI
from app.api import api_router
from app.core import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Unified Vendor Data API"}

#if __name__ == "__main__":
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8000)