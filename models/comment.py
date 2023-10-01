from beanie import Document, Link
from user import User

class Comment:

    user: Link[User]
    comment: str

    class Settings:
        name = "comments"

    