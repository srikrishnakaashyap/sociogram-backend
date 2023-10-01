from beanie import Document
from typing import Optional
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    userid: str
    description: Optional[str] = None
    age: int

class User(Document):
    name: str
    userid: str
    description: Optional[str] = None
    age: int
    access: Optional[int] = 10
    
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
    
