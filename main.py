import uvicorn
from fastapi import FastAPI, APIRouter

from app.handlers import url_router

app = FastAPI()

main_app_router = APIRouter()
main_app_router.include_router(url_router, prefix="/url", tags=["url"])

app.include_router(main_app_router)


# async def get_db():
#     async with get_async_session() as session:
#         new_url = ShortUrlORM(
#             full_url="https://www.perplexity.ai/search/python-JU9gGWCnRHdu_umso2QX9GQ",
#             short_url="assdo",
#         )
#         session.add(new_url)
#         await session.flush()
#         await session.commit()


@app.get("/ping")
async def ping():
    return {"ping": "pong"}

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)
