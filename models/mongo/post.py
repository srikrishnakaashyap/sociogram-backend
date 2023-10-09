from beanie import Document, Link
from models.mongo.user import User
from models.mongo.comment import Comment
from models.mongo.file import File
from typing import List, Optional
from pydantic import BaseModel


class Post(Document):
    user: Link[User] = None
    description: str
    comments: Optional[List[Link[Comment]]] = []
    likes: Optional[List[Link[User]]] = []
    dislikes: Optional[List[Link[User]]] = []
    files: Optional[List[Link[File]]] = None

    class Settings:
        name = "posts"