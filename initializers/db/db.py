from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from constants.GC import GC
import asyncio
from beanie import init_beanie
from models.user import User
from services.user_service import UserService

db_client: AsyncIOMotorClient = None

async def get_db() -> AsyncIOMotorClient:
    db_name = GC.DATABASE_NAME
    return db_client[db_name]


async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(GC.DATABASE_URI)
        print("connected!", await asyncio.gather(db_client.list_database_names()))
        document_models = [User]
        await init_beanie(database=await get_db(), document_models = document_models)
    except Exception as e:
        print(e)
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()
    db_client = None
    