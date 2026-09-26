from fastapi import APIRouter ,Depends , Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from src.blogapp.dtos import BlogSchema , BlogResponseSchema , UpdateBlogSchema
from src.blogapp import controllers
from src.blogapp.models import BlogModel
from src.utils.db import get_db


blog_routes = APIRouter(prefix="/blog")




@blog_routes.post("/create" , response_model=BlogResponseSchema)
def create_blog(blog:BlogSchema , db:Session = Depends(get_db)):
    return controllers.create_blog(blog , db)



@blog_routes.get("/all_blog")
def all_blog(request:Request , db:Session = Depends(get_db)):
    return controllers.all_blog(request , db)


@blog_routes.get("/blog/{blog_id}" , response_model=BlogResponseSchema)
def get_blog(blog_id:int , db:Session = Depends(get_db)):
    return controllers.get_blog(blog_id , db)




@blog_routes.post("/update")
def update_blog(blog:UpdateBlogSchema , db:Session = Depends(get_db)):
    return controllers.update_blog(blog , db)


@blog_routes.delete("/delete/{blog_id}")
def delete_blog(blog_id:int , db:Session = Depends(get_db)):
    controllers.delete_blog(blog_id , db)
