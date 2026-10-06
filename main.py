from fastapi import FastAPI 
from fastapi import Request
from src.blogapp.routers import blog_routes
from src.utils.db import Base , engine
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as starletteHTTPException
from fastapi.templating import Jinja2Templates
from src.user.routers import user_routes
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_app:FastAPI):

    #startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    #shutdown
    await engine.dispose()



app = FastAPI(lifespan=lifespan)

app.mount("/static" ,StaticFiles(directory="static") , name="static")
app.mount("/media" ,StaticFiles(directory="media") , name="media")
templates = Jinja2Templates(directory="templates")



app.include_router(blog_routes , tags=["Blogs"])
app.include_router(user_routes , tags=["Users"])




@app.exception_handler(starletteHTTPException)
def http_exception_handler(request: Request, exc: starletteHTTPException):

    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exc.status_code,
            "detail": exc.detail
        },
        status_code=exc.status_code
    )