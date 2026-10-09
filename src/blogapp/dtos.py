from pydantic import BaseModel , Field , field_serializer
from datetime import datetime , UTC
from src.user.dtos import UserResponseSchema



class BlogSchema(BaseModel):

    #user_id:int # temporary
    title:str
    content:str
    date_published: datetime = Field(
    default_factory=lambda: datetime.now(UTC).replace(tzinfo=None))

    


class BlogResponseSchema(BaseModel):

    title:str
    content:str
    id:int
    user_id:int
    date_published: datetime
    author:UserResponseSchema

    @field_serializer('date_published')
    def format_date(self, value: datetime) -> str:
        return value.strftime("%B %d, %Y").lower()


class UpdateBlogSchema(BaseModel):

    user_id:int
    title:str
    content:str


class PatchBlogSchema(BaseModel):

    title:str
    content:str


class UpdateResponseSchema(BaseModel):

    id:int
    title:str
    content:str