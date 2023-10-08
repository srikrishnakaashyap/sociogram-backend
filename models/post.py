from beanie import Document, Link
from models.user import User
from models.comment import Comment
from models.file import File
from typing import List, Optional
from pydantic import BaseModel


class Post(Document):
    user: Link[User] = None
    description: str
    comments: Optional[List[Link[Comment]]] = []
    likes: Optional[List[Link[User]]] = []
    dislikes: Optional[List[Link[User]]] = []
    media: Optional[List[Link[File]]] = None

    class Settings:

        name = "posts"

class UploadFileModel(BaseModel):
    # _id: Optional[str] = None
    name: str
    type: str
    key: str

class CreatePostModel(BaseModel):
    # _id: Optional[str] = None
    description: str
    media: Optional[List[UploadFileModel]] = None


