from typing import TypeVar

from sqlalchemy import BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from data.database import engine


class Base(AsyncAttrs, DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)

    def __repr__(self):
        tablename = self.__tablename__.capitalize().rstrip('s')
        return f'{tablename}<{self.pk}>'


class User(Base):
    __tablename__ = 'users'

    user_id = mapped_column(BigInteger, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    joined_date = mapped_column(DateTime, default=func.now())
    last_update = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    is_blocked: Mapped[bool] = mapped_column(default=False)


ModelType = TypeVar("ModelType", bound=Base)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
