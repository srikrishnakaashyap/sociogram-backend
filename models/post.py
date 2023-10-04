from beanie import Document, Link
from models.user import User
from models.comment import Comment
from models.file import File
from typing import List, Optional


class Post(Document):
    user: Link[User] = None
    description: str
    comments: Optional[List[Link[Comment]]] = []
    likes: Optional[List[Link[User]]] = []
    dislikes: Optional[List[Link[User]]] = []
    files: Optional[List[File]] = None

    class Settings:

        name = "posts"


class CreatePostModel(Document):
    description: str
    cid: Optional[str] = None
