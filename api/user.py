from typing import Annotated
from fastapi import APIRouter, Depends
from models.user import User
# from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from constants.GC import GC

router = APIRouter()

oauth2_scheme = GC.OAUTH2_SCHEME

def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
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
    user_dict = User.get(form_data.emailId)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


