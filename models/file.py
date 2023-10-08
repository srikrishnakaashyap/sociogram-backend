from pydantic import BaseModel
from typing import Optional
from beanie import Document

class File(Document):
    name: str
    type: Optional[str] = ""
    temp_link: Optional[str] = ""
    perma_link: Optional[str] = ""
    is_deleted: Optional[bool] = False