from fastapi import APIRouter

from app.schemas.url import URLItem
from app.services.url import get_or_create_url
from app.db.session import get_async_session

url_router = APIRouter()


@url_router.post("/")
async def shorten_url(body: URLItem):
    res = await get_or_create_url(body, get_async_session())
    print(res)
