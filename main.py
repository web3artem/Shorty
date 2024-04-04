import uvicorn
from fastapi import FastAPI, APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.handlers import url_router
from app.db.session import get_db
from app.services.url import get_full_url_by_short


app = FastAPI()

main_app_router = APIRouter()
main_app_router.include_router(url_router, prefix="/url", tags=["url"])

app.include_router(main_app_router)


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


@app.get("/{short_url}")
async def redirect_to_url(short_url: str, db: AsyncSession = Depends(get_db)):
    full_url = await get_full_url_by_short(short_url, db)
    return RedirectResponse(full_url)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
