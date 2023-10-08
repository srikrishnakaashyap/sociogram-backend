from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from constants.GC import GC
from services.password_service import PasswordService
from datetime import timedelta
from models.token import Token
from services.user_service import get_current_user

router = APIRouter()

oauth2_scheme = GC.OAUTH2_SCHEME


@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post('/signup', response_description="created user")
async def create(user: User)->dict:
    if await User.find_one(User.email == user.email.lower()) is None:
        user.email = user.email.lower()
        user.password = PasswordService.get_password_hash(user.password)
        response = await user.create()
        return {'message': 'user created'}
    else:
        return {'message': 'user already exists'}

@router.post('/login', response_description="user loggedin", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = await PasswordService.authenticate_user(form_data.username.lower(), form_data.password)
    print("USER", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=GC.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await PasswordService.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


