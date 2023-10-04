from beanie import Document, Link
from models.user import User

class Comment(Document):

    user: Link[User]
    comment: str

    class Settings:
        name = "comments"

    