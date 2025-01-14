import aiohttp
import asyncio

from more_itertools import chunked
from schema import CharacterSchema
from model import Characters, init_orm, close_orm
from connection import Session
from tqdm.asyncio import tqdm


MAX_REQUEST_SIZE = 20
BASE_URL = "https://swapi.py4e.com/api/people"



async def get_character(session: aiohttp.ClientSession, character_id: int):
    """Получаем основную информацию о персонаже"""
    response = await session.get(f"{BASE_URL}/{character_id}")
    response_data = await response.json()
    if response_data.get("detail"):
        return
    character = await process_character(session, response_data)
    return character


async def process_name(session: aiohttp.ClientSession, name: str):
    """Вытаскиваем одно название"""
    response = await session.get(name)
    response_data = await response.json()
    name = response_data.get("name")
    if name:
        return name
    else:
        return response_data["title"]


async def process_category(session: aiohttp.ClientSession, category: list[str]):
    """Получаем все названия"""
    if not category:
        return None
    
    elif isinstance(category, str):
        return await process_name(session, category)
    
    
    entities_to_get = [
        process_name(session, entity) 
        for entity in category
    ]

    result = await asyncio.gather(*entities_to_get)
    return ", ".join(result)




async def process_character(session: aiohttp.ClientSession, character_data: dict):
    """Заменяем ссылки на названия"""
    character_data["films"] = await process_category(session, character_data["films"])
    character_data["starships"] = await process_category(session, character_data["starships"])
    
    character_data["species"] = await process_category(session, character_data["species"])
    character_data["vehicles"] = await process_category(session, character_data["vehicles"])
    character_data["homeworld"] = await process_category(session, character_data["homeworld"])
    if character_data:
        return CharacterSchema(**character_data)


async def insetr(result: list[CharacterSchema]):
    async with Session() as session:
        objects = [Characters(**character.model_dump()) for character in result if character]
        
        session.add_all(objects)
        await session.commit()
        
    


# ================================

async def main():
    await init_orm()

    async with aiohttp.ClientSession() as session:
        
        for chunks in chunked(range(1, 88), MAX_REQUEST_SIZE):
            coros = [get_character(session, i) for i in chunks]
            result = await tqdm.gather(*coros)
            task = asyncio.create_task(insetr(result))
        
        await asyncio.wait_for(task, timeout=5)
    await close_orm()

asyncio.run(main())