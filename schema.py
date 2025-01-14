from pydantic import BaseModel, Field


class CharacterSchema(BaseModel):
    name : str = Field(
        description="Имя персонажа"
    )
    birth_year: str | None = Field(
        description="Год рождения"
    )
    eye_color: str | None = Field(
        description="Цвет глаз"
    )
    films: str = Field(
        description="Фильмы с участием"
    )
    gender: str = Field(
        description="Пол"
    )
    hair_color: str = Field(
        description="Цвет волос"
    )
    height: str = Field(
        description="Рост"
    )
    homeworld: str = Field(
        description="Родной мир"
    )
    mass: str = Field(
        description="Вес"
    )
    skin_color: str = Field(
        description="Цвет кожи"
    )
    species : str | None = Field(
        description="Вид"
    )
    starships : str | None = Field(
        description="Корабли"
    )
    vehicles : str | None = Field(
        description="Машины"
    )