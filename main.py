from fastapi import FastAPI 
from fastapi import Request
from src.blogapp.routers import blog_routes
from src.utils.db import Base , engine
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as starletteHTTPException
from fastapi.templating import Jinja2Templates
from src.user.routers import user_routes

Base.metadata.create_all(engine)

app = FastAPI()

app.mount("/static" ,StaticFiles(directory="static") , name="static")
app.mount("/media" ,StaticFiles(directory="media") , name="media")
templates = Jinja2Templates(directory="templates")



app.include_router(blog_routes)
app.include_router(user_routes)



@app.get("/")
def check():
    return {"done"}




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