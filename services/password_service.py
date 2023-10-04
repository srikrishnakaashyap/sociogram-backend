from datetime import datetime, timedelta

from jose import jwt

from constants.GC import GC
from models.user import User


class PasswordService:

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return GC.PWD_CONTEXT.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return GC.PWD_CONTEXT.hash(password)

    @classmethod
    async def create_access_token(cls, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=300)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, GC.SECRET_KEY, algorithm=GC.JWT_HASH_ALGORITHM)
        return encoded_jwt

    @classmethod
    async def authenticate_user(cls, email: str, password: str):
        user = await User.find_one(User.email == email)
        if not user:
            return False
        if not cls.verify_password(password, user.password):
            return False
        return user
