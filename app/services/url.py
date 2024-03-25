import random
from string import digits, ascii_letters
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ShortUrlORM
from app.schemas.url import URLItem, URLModelFromDB


# Creating a randomized shorten url and checking it in DB
async def shorten_url(session_factory: AsyncSession):
    async with session_factory as session:
        digits_and_letters = digits + ascii_letters
        short_url = "".join([random.choice(digits_and_letters) for _ in range(7)])

        query = (
            select(ShortUrlORM)
            .where(ShortUrlORM.short_url == short_url)
        )
        result = await session.execute(query)

        if result.scalars().one_or_none() is None:
            return short_url
        else:
            await shorten_url(session)


# Get or create entity in DB
async def get_or_create_url(body: URLItem, session: AsyncSession):
    query = (
        select(ShortUrlORM)
        .where(ShortUrlORM.full_url == body.url)
    )

    result = await session.execute(query)
    existing_entity = result.scalars().one_or_none()
    if existing_entity is None:
        short_url = await shorten_url(session)
        session.add(ShortUrlORM(full_url=body.url, short_url=short_url))
        await session.commit()
    else:
        return URLModelFromDB.model_validate(existing_entity)
