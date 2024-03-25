from pydantic import BaseModel, ConfigDict


class URLItem(BaseModel):
    url: str


class URLModelFromDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    full_url: str
    short_url: str
