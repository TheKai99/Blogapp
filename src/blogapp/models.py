from sqlalchemy import Column , Integer , String , Boolean , DateTime
from datetime import datetime
from src.utils.db import Base

class BlogModel(Base):

    __tablename__ = "Blogs"

    id = Column(Integer , primary_key=True)
    author = Column(String)
    title = Column(String)
    content = Column(String)
    date_published = Column(DateTime , default=datetime.now)
