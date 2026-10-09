from src.blogapp.dtos  import BlogResponseSchema , BlogSchema , UpdateBlogSchema , PatchBlogSchema
from sqlalchemy.orm import Session , selectinload
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.blogapp.models import BlogModel
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import HTTPException , status
from src.user.models import UserModel

templates = Jinja2Templates(directory="templates")



# Home section 
async def home(request:Request ,db:AsyncSession):
    result = await db.execute(select(BlogModel).options(selectinload(BlogModel.author)).order_by(BlogModel.date_published.desc()))
    blogs = result.scalars().all()
    return templates.TemplateResponse(request , "home.html" , {"blogs":blogs , "title":"Home"})



async def create_blog(blog: BlogSchema, db: AsyncSession , user_id:int):
    data = blog.model_dump()
    print(data)
    new_blog = BlogModel(
        user_id=user_id,
        title=data["title"],
        content=data["content"])

    db.add(new_blog)
    await db.commit()
    await db.refresh(new_blog , ["author"])

    return new_blog



#individual blog posts
async def get_blog(request: Request, blog_id: int, db: AsyncSession):
    result = await db.execute(select(BlogModel)
                    .options(selectinload(BlogModel.author))
                    .where(BlogModel.id == blog_id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    return templates.TemplateResponse(request, "post.html", {"blog": blog, "title": "blog"})
    


async def update_blog_fully(blog_id: int, blog: UpdateBlogSchema, db: AsyncSession):
    data = blog.model_dump()

    result = await db.execute(select(BlogModel).where(BlogModel.id == blog_id))
    is_blog = result.scalar_one_or_none()

    if not is_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    result = await db.execute(select(BlogModel).where(BlogModel.user_id == data['user_id']))
    is_user = result.scalar_one_or_none()

    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="there is no user with this id")

    is_blog.user_id = data['user_id']
    is_blog.title = data['title']
    is_blog.content = data['content']

    await db.commit()
    await db.refresh(is_blog)

    return is_blog


async def update_blog_partially(blog_id: int, blog: PatchBlogSchema, db: AsyncSession):

    result = await db.execute(select(BlogModel).where(BlogModel.id == blog_id))
    is_blog = result.scalar_one_or_none()

    if not is_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    data = blog.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(is_blog, field, value)

    await db.commit()
    await db.refresh(is_blog)

    return is_blog


async def delete_blog(blog_id: int, db: AsyncSession):

    result = await db.execute(select(BlogModel).where(BlogModel.id == blog_id))
    is_blog = result.scalar_one_or_none()

    if not is_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

    await db.delete(is_blog)
    await db.commit()

    print(f"Deleted blog with ID: {blog_id}")

    return None


# All the blogs regarding a specific user 
async def user_blog_page(request , user_id:int , db:AsyncSession):

    response = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = response.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not found")

    result = await db.execute(select(BlogModel)
                              .options(selectinload(BlogModel.author))
                              .where(BlogModel.user_id == user_id).order_by(BlogModel.date_published.desc()))
    
    blogs = result.scalars().all()

    return templates.TemplateResponse(request ,"user_posts.html" , {"blogs":blogs , "user":user , "title":f"{user.username}blog's"} )



async def get_all_blogs(db:AsyncSession):
    result = await db.execute(select(BlogModel))
    all_blogs = result.scalars().all()
    return all_blogs