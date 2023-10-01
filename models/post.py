from beanie import Document, Link
from user import User
from comment import Comment
from typing import List

class Post(Document):
    user: Link[User]
    description: str
    comments: List[Link[Comment]] = []
    likes: List[Link[User]] = []
    dislikes: List[Link[User]] = []


    class Settings:

        name = "posts"

