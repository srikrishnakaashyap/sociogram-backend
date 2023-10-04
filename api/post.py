from fastapi import APIRouter, Depends, HTTPException, status
from models.post import Post, CreatePostModel
from models.user import User
from models.file import File
from typing import Annotated
from services.user_service import get_current_user


router = APIRouter()

@router.post('/post', response_description="created post")
async def create(post: CreatePostModel, user:Annotated[User, Depends(get_current_user)])->dict:
    files = [File(temp_link=post.cid)]
    post_model = Post(user=user, description=post.description, files=files)
    response = await post_model.create()
    return {'message': 'post created'}

@router.post('/updatePost', response_description="updated post")
async def update(post: Post)->dict:
    if await Post.find_one(Post.id == post.id) is None:
        return {'message': 'post not found'}