from fastapi import FastAPI
from src.blogapp.routers import blog_routes
from src.utils.db import Base , engine
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(engine)

app = FastAPI()

app.mount("/static" ,StaticFiles(directory="static") , name="static")


app.include_router(blog_routes)



@app.get("/")
def check():
    return {"done"}