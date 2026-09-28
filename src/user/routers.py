from fastapi import APIRouter , Depends
from src.user import controllers
from src.user.dtos import UserSchema , UserResponseSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db




user_routes = APIRouter(prefix="/user")



@user_routes.post("/create" , response_model=UserResponseSchema)
def create_user(data:UserSchema , db:Session = Depends(get_db)):
    return controllers.create_user(data , db)

@user_routes.get("/get_user/{user_id}" , response_model=UserResponseSchema)
def get_user(user_id:int , db:Session = Depends(get_db)):
    return controllers.get_user(user_id , db)