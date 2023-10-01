from fastapi import APIRouter, Depends
from services.user_service import UserService

router = APIRouter()


@router.get('/', include_in_schema=False)
async def create():
    user = await UserService.create_user(user_props={'name': 'test', 'age': 19, 'id': 'test1'})
    print(user)
    return {'message': 'user created'}


