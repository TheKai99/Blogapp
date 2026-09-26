from src.blogapp.dtos  import BlogResponseSchema , BlogSchema , UpdateBlogSchema
from sqlalchemy.orm import Session
from src.blogapp.models import BlogModel
from fastapi.templating import Jinja2Templates
from fastapi import Request


templates = Jinja2Templates(directory="templates")

def create_blog(blog:BlogSchema , db:Session):
    data = blog.model_dump()

    new_blog = BlogModel(
        author = data["author"],
        title = data["title"],
        content = data["content"],
        date_published = data["date_published"])

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog



def all_blog(request:Request ,db:Session):
    blogs = db.query(BlogModel).all()
    return templates.TemplateResponse(request , "home.html" , {"blogs":blogs , "title":"Home"})

def get_blog(blog_id:int , db:Session):

    is_blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()

    if not is_blog:
        return {"invalid id oops"}

    return is_blog
    


def update_blog(blog:UpdateBlogSchema , db:Session):

    data = blog.model_dump()

    is_blog = db.query(BlogModel).filter(BlogModel.id == data["id"]).first()

    if not is_blog:
        return {"the blog with this id not exist"}



    is_blog.author = data["author"]
    is_blog.title = data["title"]
    is_blog.content = data["content"]
    is_blog.date_published = data["date_published"]

    db.commit()
    db.refresh(is_blog)

    return {"msg":"task updated successfully" , "updated":is_blog}


def delete_blog(blog_id:int , db:Session):

    is_blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()

    if not is_blog:
        return {"your blog id in invalid"}

    db.delete(is_blog)
    db.commit()

    return {"msg":"blog deleted successfully"}