from fastapi import APIRouter, Depends, HTTPException, status, Form
from models.post import Post, CreatePostModel
from models.user import User
from models.file import File
from typing import Annotated
from services.user_service import get_current_user



router = APIRouter()

@router.post('/post', response_description="created post")
async def create(user:Annotated[User, Depends(get_current_user)], post: CreatePostModel)->dict:

    print("POST", post)
    media = post.media
    file_objects = []
    for m in media:
        file = File( **{"name":m.name,"type":m.type, "temp_link":f"https://file.io/{m.key}" })
        file_objects.append(file)
    
    await File.insert_many(file_objects)
    post_model = Post(user=user, description=post.description, files=file_objects)
    response = await post_model.create()
    # updateFiles(file_objects)
    return {'message': 'post created'}

@router.post('/updatePost', response_description="updated post")
async def update(post: Post)->dict:
    if await Post.find_one(Post.id == post.id) is None:
        return {'message': 'post not found'}