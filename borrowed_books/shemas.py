from datetime import date
from pydantic import BaseModel


class SBorrowedBooks(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: date
    return_date: date

class SBorrowedBooksModel(BaseModel):
    book_id: int
    borrow_date: date

class SBorrowedBooksReturnModel(BaseModel):
    book_id: int
    return_date: date