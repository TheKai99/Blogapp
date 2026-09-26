from pydantic import BaseModel , Field , field_serializer
from datetime import datetime



class BlogSchema(BaseModel):

    author:str
    title:str
    content:str
    date_published: datetime = Field(default_factory=datetime.now)

    


class BlogResponseSchema(BaseModel):

    title:str
    content:str
    date_published: datetime

    @field_serializer('date_published')
    def format_date(self, value: datetime) -> str:
        return value.strftime("%#I:%M %p %#d %B %Y").lower()


class UpdateBlogSchema(BaseModel):

    id:int
    author:str
    title:str
    content:str
    date_published: datetime = Field(default_factory=datetime.now)