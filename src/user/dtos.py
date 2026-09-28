from pydantic import BaseModel , Field , EmailStr


class UserSchema(BaseModel):

    username:str = Field(min_length=1 , max_length=120)
    email:EmailStr = Field(max_length=120)
    image_file:str


class UserResponseSchema(BaseModel):

    id:int
    username:str
    email:EmailStr
    image_file:str | None = None
    image_path:str




    