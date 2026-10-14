from fastapi import APIRouter , Depends , status , Request
from src.user import controllers
from src.user.dtos import UserSchema , UserResponseSchema , UserUpdateSchema , UserLoginSchema
from sqlalchemy.orm import Session
from src.utils.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

templates = Jinja2Templates(directory="templates")

user_routes = APIRouter(prefix="/user")


@user_routes.get("/register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        request,
        "register.html"
    )

@user_routes.get("/login")
async def login_page(request:Request):
    return templates.TemplateResponse(
        request , "login.html"
    )


@user_routes.post("/register" , response_model=UserResponseSchema)
async def register_user(request:Request , data:UserSchema , db:AsyncSession = Depends(get_db)):
    return await controllers.register_user(request , data , db)

@user_routes.post("/login")
async def login_user(form_data:Annotated[OAuth2PasswordRequestForm , Depends()] , db:AsyncSession = Depends(get_db)):
    return await controllers.login_user(form_data ,  db)


@user_routes.get("/me" , response_model=UserResponseSchema)
async def get_current_user(token:Annotated[str , 
                    Depends(oauth2_scheme)] ,
                    db:Annotated[AsyncSession , Depends(get_db)]):
    return await controllers.get_current_user(token , db)


@user_routes.get("/get/{user_id}" , response_model=UserResponseSchema)
async def get_user(user_id:int , db:AsyncSession = Depends(get_db)):
    return await controllers.get_user(user_id , db)


@user_routes.patch("/update/{user_id}")
async def update_user(user_id:int , data:UserUpdateSchema , db:AsyncSession = Depends(get_db)):
    return await controllers.update_user(user_id , data , db)


#delete the user
@user_routes.delete("/delete/{user_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id:int , db:AsyncSession = Depends(get_db)):
    return await controllers.delete_user(user_id , db)
