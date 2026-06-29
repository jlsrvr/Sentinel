from fastapi import APIRouter

router = APIRouter(prefix="/cases", tags=["cases"])

@app.get("/cases/")
async def read_case(skip: int = 0, limit: int = 20):
    return fake_items_db[skip : skip + limit]