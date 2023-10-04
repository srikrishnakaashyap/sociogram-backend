from beanie import Document, Link
from models.user import User
from models.comment import Comment
from typing import List

class Post(Document):
    user: Link[User] = None
    description: str
    comments: List[Link[Comment]] = []
    likes: List[Link[User]] = []
    dislikes: List[Link[User]] = []


    class Settings:

        name = "posts"

