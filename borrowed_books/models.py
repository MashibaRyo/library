from sqlalchemy import Column, Integer, ForeignKey, Date
from database import Base

class BorrowedBooks(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reader_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    borrow_date = Column(Date, nullable=False)
    return_date = Column(Date, default=None)