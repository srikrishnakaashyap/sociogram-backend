from beanie import Document
from typing import Optional

class User(Document):
    name: str
    id: str
    description: Optional[str] = None
    age: int
    access: int
    
    class Settings:
        name = "users"
    
