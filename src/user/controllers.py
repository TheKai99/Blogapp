from fastapi import HTTPException ,status , Depends , Request
from sqlalchemy.orm import Session
from src.user.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , func
from src.user.dtos import UserSchema , UserUpdateSchema , UserLoginSchema , ChangePassword
from src.utils.settings import settings
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime
from datetime import timedelta
from fastapi.templating import Jinja2Templates
from src.utils.image_utils import process_profile_image , delete_profile_image
from PIL import UnidentifiedImageError
from starlette.concurrency import run_in_threadpool

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


async def update_profile_pic(file , current_user , db):
    
    content = await file.read()

    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"file to large the accepted size is {settings.MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB")

    try:
        new_filename = await run_in_threadpool(process_profile_image , content)

    except UnidentifiedImageError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file , upload a valid image",
        ) from err

    result = await db.execute(select(UserModel).where(UserModel.id == current_user))
    user = result.scalar_one_or_none()

    old_filename = user.image_file

    user.image_file = new_filename

    await db.commit()
    await db.refresh(user)


    if old_filename:
        delete_profile_image(old_filename)

    return user


async def change_password(data:ChangePassword , current_user , db):
    result =await db.execute(select(UserModel).where(UserModel.id == current_user))
    user = result.scalar_one_or_none()

    user_data = data.model_dump()
    user_current_pass = user_data["current_pass"]


    if not verify_password(user_current_pass ,user.password_hash):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="your current pass is not correct")

    new_pass = user_data["new_pass"]
    confirm_pass = user_data["confirm_new_pass"]

    if(new_pass != confirm_pass):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="you new pass not equal to the confirm pass check it ")

    new_hashed_pass = get_password_hash(confirm_pass)

    user.password_hash = new_hashed_pass
    await db.commit()
    await db.refresh(user)

    return "password changed successfully"



