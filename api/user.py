from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from models.user import User
# from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from constants.GC import GC

router = APIRouter()

oauth2_scheme = GC.OAUTH2_SCHEME

def fake_decode_token(token):
    return User.find_one(User.email == token)

def fake_hash_password(password: str):
    return "fakehashed" + password

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = await fake_decode_token(token)
    return user


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post('/signup', response_description="created user")
async def create(user: User)->dict:
    response = await user.create()
    print(response)
    return {'message': 'user created'}

@router.post('/login', response_description="user loggedin")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = await User.find_one(User.email==form_data.username)
    print("user_dict",user_dict)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user_password = fake_hash_password(user_dict.password)
    hashed_password = fake_hash_password(form_data.password)
    print("userPass",user_password)
    print("haspas",hashed_password)
    if not hashed_password == user_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_dict.email, "token_type": "bearer"}


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


