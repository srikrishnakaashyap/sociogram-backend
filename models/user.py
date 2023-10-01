from beanie import Document
from typing import Optional
from pydantic import EmailStr


class User(Document):
    name: str
    description: Optional[str] = None
    age: int
    access: Optional[int] = 10
    email: str
    password: str
    userId: Optional[str] = None
    
    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "name": "fname lname",
                "userid": "flname",
                "description": "Hi",
                "age": 20,
                "access": 10
            }
        }
    
