from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import String, Integer
from connection import engine

class Base(DeclarativeBase, AsyncAttrs):

    pass


class Characters(Base):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    birth_year: Mapped[str] = mapped_column(String)
    eye_color: Mapped[str] = mapped_column(String)
    films: Mapped[str] = mapped_column(String)
    gender: Mapped[str] = mapped_column(String)
    hair_color: Mapped[str] = mapped_column(String)
    height: Mapped[str] = mapped_column(String)
    homeworld: Mapped[str] = mapped_column(String)
    mass: Mapped[str] = mapped_column(String)
    skin_color: Mapped[str] = mapped_column(String)
    species : Mapped[str] = mapped_column(String, nullable=True)
    starships : Mapped[str] = mapped_column(String, nullable=True)
    vehicles : Mapped[str] = mapped_column(String, nullable=True)


async def init_orm():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()