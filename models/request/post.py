from typing import List, Optional
from pydantic import BaseModel

class UploadFileModel(BaseModel):
    # _id: Optional[str] = None
    name: str
    type: str
    key: str

class CreatePostModel(BaseModel):
    # _id: Optional[str] = None
    description: str
    media: Optional[List[UploadFileModel]] = None