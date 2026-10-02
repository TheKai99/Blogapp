from fastapi import HTTPException ,status
from sqlalchemy.orm import Session
from src.user.models import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.user.dtos import UserSchema , UserUpdateSchema




async def create_user(data:UserSchema , db:AsyncSession):

    user_data = data.model_dump()

    result = await db.execute(select(UserModel).where(UserModel.username == user_data["username"]))
    is_user = result.scalar_one_or_none()
    
    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="username already exist cant make user")


    result = await db.execute(select(UserModel).where(UserModel.email == user_data["email"]))
    is_user = result.scalar_one_or_none()

    if is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="email already exist try with another")

    

    new_user = UserModel(
        username = user_data['username'],
        email = user_data['email'],
        image_file = user_data['image_file']


    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    

    return new_user


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