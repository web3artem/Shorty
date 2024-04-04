import random
from string import digits, ascii_letters
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ShortUrlORM
from app.schemas.url import URLItem, URLModelFromDB


# Creating a randomized shorten url and checking it in DB
async def shorten_url(session_factory):
    digits_and_letters = digits + ascii_letters
    short_url = "".join([random.choice(digits_and_letters) for _ in range(7)])
    query = select(ShortUrlORM).where(ShortUrlORM.short_url == short_url)
    result = await session_factory.execute(query)
    if result.scalars().one_or_none() is None:
        return short_url
    else:
        await shorten_url(session_factory)


# Get or create entity in DB
async def get_or_create_url(body: URLItem, session_factory: AsyncSession):
    query = select(ShortUrlORM).where(ShortUrlORM.full_url == body.url)
    result = await session_factory.execute(query)
    existing_entity = result.scalars().one_or_none()
    if existing_entity is None:
        short_url = await shorten_url(session_factory)
        session_factory.add(ShortUrlORM(full_url=body.url, short_url=short_url))
        await session_factory.commit()
        return short_url
    else:
        return URLModelFromDB.model_validate(existing_entity).short_url


async def get_full_url_by_short(short_url: str, session: AsyncSession):
    query = select(ShortUrlORM.full_url).where(ShortUrlORM.short_url == short_url)
    # print(query.compile(compile_kwargs={"literal_binds": True}))
    result = await session.execute(query)
    return result.scalars().first()
