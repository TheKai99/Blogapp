from fastapi import APIRouter ,Depends , Request ,status
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from src.blogapp.dtos import BlogSchema , BlogResponseSchema , UpdateBlogSchema , PatchBlogSchema
from src.blogapp import controllers
from src.blogapp.models import BlogModel
from src.utils.db import get_db
from src.utils.dependency import get_current_user_id


blog_routes = APIRouter(prefix="/blog")



# creating blog
@blog_routes.post("/create" , response_model=BlogResponseSchema)
async def create_blog(blog:BlogSchema , db:AsyncSession = Depends(get_db) , user_id:int = Depends(get_current_user_id)):
    return await controllers.create_blog(blog , db , user_id)


#Home section
@blog_routes.get("/home")
async def home(request:Request , db:AsyncSession = Depends(get_db)):
    return await controllers.home(request , db)


# get a single blog
@blog_routes.get("/{blog_id}" , response_model=BlogResponseSchema)
async def get_blog(request:Request ,blog_id:int , db:AsyncSession = Depends(get_db)):
    return await  controllers.get_blog(request ,blog_id , db)


#update the blog fully
@blog_routes.put("/{blog_id}", response_model=BlogResponseSchema)
async def update_blog_fully(blog_id:int , blog:UpdateBlogSchema , db:AsyncSession = Depends(get_db)):
    return await controllers.update_blog_fully(blog_id , blog , db)


#update blog partially
@blog_routes.patch("/{blog_id}", response_model=BlogResponseSchema)
async def update_blog_partially(blog_id:int , blog:PatchBlogSchema , db:AsyncSession = Depends(get_db)):
    return await controllers.update_blog_partially(blog_id , blog , db)


#delete the blog
@blog_routes.delete("/{blog_id}" , status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id:int , db:AsyncSession = Depends(get_db)):
    return await controllers.delete_blog(blog_id , db)


#User posts page
@blog_routes.get("/{user_id}/blogs")
async def user_blog_page(request:Request , user_id:int , db:AsyncSession = Depends(get_db)):
    return await controllers.user_blog_page(request ,user_id , db)



#get all the blogs
@blog_routes.get("/api/all")
async def get_all_blogs(request:Request ,db:AsyncSession = Depends(get_db)):
    return await controllers.get_all_blogs(db)