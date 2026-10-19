from fastapi import HTTPException ,status , Depends , Request
from sqlalchemy.orm import Session
from src.user.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , func
from src.user.dtos import UserSchema , UserUpdateSchema , UserLoginSchema
from src.utils.settings import settings
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime
from datetime import timedelta
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


hash_password = PasswordHash.recommended()

def get_password_hash(password):
    return hash_password.hash(password)

def verify_password(plain_password , hashed_password):
    return hash_password.verify(plain_password , hashed_password)




async def register_user(request , data:UserSchema , db:AsyncSession):

    user_data = data.model_dump()

    result = await db.execute(select(UserModel).where(func.lower(UserModel.username) == user_data["username"].lower()))
    is_user = result.scalar_one_or_none()
    
    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="username already exist cant make user")

    result = await db.execute(select(UserModel).where(func.lower(UserModel.email) == user_data["email"].lower()))
    is_user = result.scalar_one_or_none()

    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="email already exist try with another")

    hash_password = get_password_hash(user_data["password"])

    print(hash_password)

    new_user = UserModel(
        username = user_data['username'],
        email = user_data['email'].lower(),
        password_hash = hash_password,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def login_user(form_data:Annotated[OAuth2PasswordRequestForm , Depends()] , db:AsyncSession):

    result = await db.execute(select(UserModel).where(UserModel.email == form_data.username.lower()))
    is_user = result.scalar_one_or_none()

    if not  is_user or not verify_password(form_data.password , is_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is wrong!",
            headers={"WWW-Authenticate": "Bearer"})

    exp_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"_id":is_user.id , "exp":exp_time}
    token = jwt.encode(to_encode , settings.SECRET_KEY , settings.ALGORITHM)
    print(token)

    return {"access_token": token, "token_type": "bearer"}


async def get_current_user(token , db):

    try:
        payload = jwt.decode(token , settings.SECRET_KEY , algorithms=settings.ALGORITHM)
        user_id = payload["_id"]

    except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="token expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="invalid token")

    result = await db.execute(select(UserModel).where(UserModel.id == int(user_id)))
    is_user = result.scalar_one_or_none()

    if is_user is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User not found")

    return is_user
    


async def get_user(user_id:int , db:AsyncSession):

    result = await db.execute(select(UserModel).where(UserModel.id == user_id))

    is_user = result.scalar_one_or_none()

    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not exist")


    return is_user


async def update_user(user_id, data: UserUpdateSchema, db: AsyncSession):

    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    is_user = result.scalar_one_or_none()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if data.email:
        result = await db.execute(select(UserModel).where(UserModel.email == data.email , UserModel.id != user_id) )
        email_exist = result.scalar_one_or_none()
        if email_exist:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="email already exist try another")

    if data.username:
            result = await db.execute(select(UserModel).where(UserModel.username == data.username , UserModel.id != user_id) )
            username = result.scalar_one_or_none()
            if username:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="username already exist try another")

    user_data = data.model_dump(exclude_unset=True)

    for field, value in user_data.items():
        setattr(is_user, field, value)

    await db.commit()
    await db.refresh(is_user)
    return is_user



async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    is_user = result.scalar_one_or_none()

    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="there is no user with this id")

    await db.delete(is_user)
    await db.commit()

    return None