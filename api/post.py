from fastapi import APIRouter, Depends, HTTPException, status, Form
from models.mongo.post import Post
from models.request.post import CreatePostModel
from models.mongo.user import User
from models.mongo.file import File
from typing import Annotated
from services.user_service import get_current_user
from services.media_storage import MediaStorage


router = APIRouter()


@router.post('/post', response_description="created post")
async def create(user: Annotated[User, Depends(get_current_user)], post: CreatePostModel) -> dict:
    file_links = []
    print("POST", post)
    media = post.media
    file_objects = []
    for m in media:
        file = File(**{"name": m.name, "type": m.type,
                    "temp_link": f"https://file.io/{m.key}"})
        file_objects.append(file)

    file_objects_op = await File.insert_many(file_objects)
    post_model = Post(user=user, description=post.description,
                      files=file_objects_op.inserted_ids)
    response = await post_model.create()
    # updateFiles(file_objects)

    try:
        return {'message': 'post created'}
    finally:
        await MediaStorage.fileio_to_s3(file_objects_op.inserted_ids)


@router.post('/updatePost', response_description="updated post")
async def update(post: Post) -> dict:
    if await Post.find_one(Post.id == post.id) is None:
        return {'message': 'post not found'}
