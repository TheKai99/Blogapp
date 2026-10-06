from fastapi import APIRouter , Depends , status
from src.user import controllers
from src.user.dtos import UserSchema , UserResponseSchema , UserUpdateSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession




user_routes = APIRouter(prefix="/user")



@user_routes.post("/create" , response_model=UserResponseSchema)
async def create_user(data:UserSchema , db:AsyncSession = Depends(get_db)):
    return await controllers.create_user(data , db)

@user_routes.get("/{user_id}" , response_model=UserResponseSchema)
async def get_user(user_id:int , db:AsyncSession = Depends(get_db)):
    return await controllers.get_user(user_id , db)

@user_routes.patch("/{user_id}")
async def update_user(user_id:int , data:UserUpdateSchema , db:AsyncSession = Depends(get_db)):
    return await controllers.update_user(user_id , data , db)


#delete the user
@user_routes.delete("/delete/{user_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int , db:AsyncSession = Depends(get_db)):
    return await controllers.delete_user(user_id , db)
