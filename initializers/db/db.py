from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from constants.GC import GC
import asyncio
from beanie import init_beanie
from models.mongo.user import User
from models.mongo.post import Post
from models.mongo.file import File
from models.mongo.comment import Comment

# db_client: AsyncIOMotorClient = None


async def get_db() -> AsyncIOMotorClient:
    db_name = GC.DATABASE_NAME
    return db_client[db_name]


async def connect_and_init_db():
    global db_client
    try:
        db_client = AsyncIOMotorClient(GC.DATABASE_URI)
        print("connected!", await asyncio.gather(db_client.list_database_names()))
        document_models = [User, Post, File, Comment]
        await init_beanie(database=await get_db(), document_models=document_models)
    except Exception as e:
        print(e)
        raise


async def close_db_connect():
    global db_client
    if db_client is None:
        return
    db_client.close()
    db_client = None
