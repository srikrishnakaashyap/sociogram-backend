from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from constants.GC import GC
from services.password_service import PasswordService
from datetime import timedelta
from models.post import Post
from models.file import File
from services.user_service import get_current_user

router = APIRouter()

@router.get("/test")
async def test():

    post = await Post.get("6522e903051473f1b7c67e99", fetch_links=True)
    files = post.files

    return {"response":files}
