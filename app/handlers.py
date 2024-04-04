from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.url import URLItem
from app.services.url import get_or_create_url
from app.db.session import get_db

url_router = APIRouter()


@url_router.post("/")
async def create_short_url(body: URLItem, db: AsyncSession = Depends(get_db)):
    res = await get_or_create_url(body, db)
    return JSONResponse(
        content={"message": f"127.0.0.1:8001/{res}"}, status_code=200
    )
