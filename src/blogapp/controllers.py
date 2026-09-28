from src.blogapp.dtos  import BlogResponseSchema , BlogSchema , UpdateBlogSchema
from sqlalchemy.orm import Session
from src.blogapp.models import BlogModel
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import HTTPException , status
from src.user.models import UserModel

templates = Jinja2Templates(directory="templates")

def create_blog(blog:BlogSchema , db:Session):
    data = blog.model_dump()

    new_blog = BlogModel(
        user_id = data["user_id"],
        title = data["title"],
        content = data["content"],
        date_published = data["date_published"])

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog


# Home section 
def home(request:Request ,db:Session):
    blogs = db.query(BlogModel).all()
    return templates.TemplateResponse(request , "home.html" , {"blogs":blogs , "title":"Home"})



#individual blog posts
def get_blog(request:Request ,blog_id:int , db:Session):
    blog = db.query(BlogModel).filter(BlogModel.id == blog_id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Page not found")

    return templates.TemplateResponse(request ,"post.html" , {"blog":blog , "title":"blog"} )
    


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



def user_blog_page(request ,user_id:int , db:Session):

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not found")

    result = db.query(BlogModel).filter(BlogModel.user_id == user_id).all()

    return templates.TemplateResponse(request ,"user_posts.html" , {"blogs":result , "user":user , "title":f"{user.username}blog's"} )

