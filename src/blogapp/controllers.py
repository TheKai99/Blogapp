from src.blogapp.dtos  import BlogResponseSchema , BlogSchema , UpdateBlogSchema , PatchBlogSchema
from sqlalchemy.orm import Session , selectinload
from sqlalchemy import select , func
from sqlalchemy.ext.asyncio import AsyncSession
from src.blogapp.models import BlogModel
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import HTTPException , status
from src.user.models import UserModel

templates = Jinja2Templates(directory="templates")



# Home section 
async def home(request:Request ,page,db:AsyncSession):

    limit = 8
    offset = (page-1)*limit

    check = await db.execute(select(func.count()).select_from(BlogModel))
    total = check.scalar_one() or 0

    result = await db.execute(select(BlogModel)
                        .options(selectinload(BlogModel.author))
                        .order_by(BlogModel.date_published.desc()).offset(offset).limit(limit))
    blogs = result.scalars().all()
    return templates.TemplateResponse(request , "home.html" , {"blogs":blogs , "title":"Home",
                                                               "page":page,
                                                               "total":total,
                                                               "has_previous":page>1,
                                                               "has_next":offset + len(blogs) < total})



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

from src.utils.dependency import get_current_user_id

#individual blog posts
async def get_blog(request: Request, blog_id: int,  db: AsyncSession):
    result = await db.execute(select(BlogModel)
                    .options(selectinload(BlogModel.author))
                    .where(BlogModel.id == blog_id))
    blog = result.scalar_one_or_none()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Page not found")

    return templates.TemplateResponse(request, "post.html", {"blog": blog,
                                                              "title": "blog"})
    


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


async def update_blog_partially(blog_id: int, blog: PatchBlogSchema, user_id:int , db: AsyncSession , ):

    result = await db.execute(select(BlogModel)
                              .options(selectinload(BlogModel.author))
                              .where(BlogModel.user_id == user_id,
                                     BlogModel.id == blog_id))
    
    is_blog = result.scalar_one_or_none()

    if not is_blog:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="not allowed to edit this post!")


    data = blog.model_dump(exclude_unset=True)

    for field, value in data.items():
        setattr(is_blog, field, value)

    await db.commit()
    await db.refresh(is_blog)

    return is_blog


async def delete_blog(blog_id: int,user_id:int ,  db: AsyncSession):

    result = await db.execute(select(BlogModel)
                              .options(selectinload(BlogModel.author))
                              .where(BlogModel.id == blog_id,
                                    BlogModel.user_id == user_id))
    
    is_blog = result.scalar_one_or_none()

    if not is_blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="blog not found")

    await db.delete(is_blog)
    await db.commit()

    print(f"Deleted blog with ID: {blog_id}")

    return None


# All the blogs regarding a specific user 
async def user_blog_page(request , user_id ,page , db:AsyncSession):

    limit = 2
    offset = (page-1)*limit

    response = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = response.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="user not found")

    check = await db.execute(select(func.count()).select_from(BlogModel).where(BlogModel.user_id == user_id))
    total = check.scalar_one()

    result = await db.execute(select(BlogModel)
                              .options(selectinload(BlogModel.author))
                              .where(BlogModel.user_id == user_id).order_by(BlogModel.date_published.desc()).offset(offset).limit(limit))
    
    blogs = result.scalars().all()

    return templates.TemplateResponse(request ,"user_posts.html" , {"blogs":blogs ,
                                                                    "user":user ,
                                                                    "title":f"{user.username}blog's",
                                                                    "page":page,
                                                                    "total":total,
                                                                    "has_previous":page>1,
                                                                    "has_next":offset + len(blogs) < total} )



async def get_all_blogs(page , db:AsyncSession):

    limit = 4
    offset = (page-1)*limit
    check = await db.execute(select(func.count()).select_from(BlogModel))
    total = check.scalar_one()

    result = await db.execute(select(BlogModel).order_by(BlogModel.date_published.desc()).offset(offset).limit(limit))
    all_blogs = result.scalars().all()
    return all_blogs , total