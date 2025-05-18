from sqlalchemy import Column, Integer, String
from database import Base

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer, nullable=True)
    ISBN = Column(Integer, unique=True, nullable=True)
    quantity = Column(Integer, nullable=True, default=1)
    description = Column(String, nullable=True)