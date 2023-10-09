import pymongo
from beanie import Document, Indexed
from typing import Optional
from pydantic import EmailStr


class User(Document):
    name: str
    description: Optional[str] = None
    age: int
    access: Optional[int] = 10
    email: Indexed(str, index_type=pymongo.TEXT)
    password: str
    userId: Optional[str] = None

    def __repr__(self) -> str:
        return self.email+self.password
    
    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "name": "fname lname",
                "userid": "flname",
                "description": "Hi",
                "age": 20,
                "access": 10,
                "password": "***"
            }
        }
    
