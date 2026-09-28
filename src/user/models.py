from sqlalchemy import Column , Integer , String , Boolean , DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.utils.db import Base

class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer , primary_key=True ,index=True)
    username = Column(String , unique=True , nullable=False)
    email = Column(String , unique=True , nullable=False)
    image_file = Column(String , unique=False , nullable=True ,default=None )



# Relationship: lets you do user.blogs to get all their blogs
    blogs = relationship("BlogModel" , back_populates="author")




    @property
    def image_path(self):
        if self.image_file:
            return f"/media/profile_pics/{self.image_file}"
        return "/static/profile_pics/default.jpg"
