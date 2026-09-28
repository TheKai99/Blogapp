from sqlalchemy import Column , Integer , String , Boolean , DateTime , ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from src.utils.db import Base

class BlogModel(Base):

    __tablename__ = "blogs"

    id = Column(Integer , primary_key=True)
    #author = Column(String)  let temporarly erase it as i can acces the same thing by blog.owner.username
    title = Column(String)
    content = Column(String)
    date_published = Column(DateTime , default=datetime.now)



# Foreign key for one - many relationship between the Users and Blogs
    user_id  = Column(Integer , ForeignKey("users.id") , nullable=False)


# to get the author or owner info we can use  blog.author  to get Userobject
    author = relationship("UserModel" , back_populates="blogs")
