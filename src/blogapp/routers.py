from fastapi import APIRouter ,Depends , Request ,status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from src.blogapp.dtos import BlogSchema , BlogResponseSchema , UpdateBlogSchema , PatchBlogSchema
from src.blogapp import controllers
from src.blogapp.models import BlogModel
from src.utils.db import get_db


blog_routes = APIRouter(prefix="/blog")



# creating blog
@blog_routes.post("/create" , response_model=BlogResponseSchema)
def create_blog(blog:BlogSchema , db:Session = Depends(get_db)):
    return controllers.create_blog(blog , db)


#Home section
@blog_routes.get("/home")
def home(request:Request , db:Session = Depends(get_db)):
    return controllers.home(request , db)


# get a single blog
@blog_routes.get("/{blog_id}" , response_model=BlogResponseSchema)
def get_blog(request:Request ,blog_id:int , db:Session = Depends(get_db)):
    return controllers.get_blog(request ,blog_id , db)


#update the blog fully
@blog_routes.put("/{blog_id}", response_model=BlogResponseSchema)
def update_blog_fully(blog_id:int , blog:UpdateBlogSchema , db:Session = Depends(get_db)):
    return controllers.update_blog_fully(blog_id , blog , db)


#update blog partially
@blog_routes.patch("/{blog_id}", response_model=BlogResponseSchema)
def update_blog_partially(blog_id:int , blog:PatchBlogSchema , db:Session = Depends(get_db)):
    return controllers.update_blog_partially(blog_id , blog , db)


#delete the blog
@blog_routes.delete("/{blog_id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id:int , db:Session = Depends(get_db)):
    controllers.delete_blog(blog_id , db)


#User posts page
@blog_routes.get("/{user_id}/blogs")
def user_blog_page(request:Request , user_id:int , db:Session = Depends(get_db)):
    return controllers.user_blog_page(request ,user_id , db)



#get all the blogs
@blog_routes.get("/api/all")
def get_all_blogs(db:Session = Depends(get_db)):
    return controllers.get_all_blogs(db)