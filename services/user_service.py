from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from jose import JWTError, jwt

from constants.GC import GC
from models.token import TokenData
from models.user import User



async def get_current_user(token: Annotated[str, Depends(GC.OAUTH2_SCHEME)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, GC.SECRET_KEY, algorithms=[GC.JWT_HASH_ALGORITHM])
        print(payload.get("exp"))
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(email=username)
    except JWTError:
        raise credentials_exception
    user = await User.find_one(User.email == token_data.email)
    if user is None:
        raise credentials_exception
    
    print("USER", user)
    return user




    


