import asyncio

from fastapi import FastAPI
from fastapi import Depends

from app.core.config import settings

app = FastAPI()

from app.db.session import get_async_session
from app.db.models import ShortUrlORM, Base


async def get_db():
    async with get_async_session() as session:
        new_url = ShortUrlORM(full_url="https://www.perplexity.ai/search/python-JU9gGWCnRHu_umso2QX9GQ",
                              short_url="asdo")
        session.add(new_url)
        await session.flush()
        await session.commit()


@app.get("/")
async def root():
    return {"message": "Hello world!"}


print(settings.DATABASE_URL)
asyncio.run(get_db())
