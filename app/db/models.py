from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


intpk = Annotated[int, mapped_column(primary_key=True)]


class ShortUrlORM(Base):
    __tablename__ = "urls"

    id: Mapped[intpk]
    full_url: Mapped[str] = mapped_column(unique=True)
    short_url: Mapped[str] = mapped_column(unique=True)
