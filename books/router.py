from fastapi import APIRouter, Depends, HTTPException

from books.dao import BooksDAO
from books.shemas import SBooksModel
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.get("{book_id}")
async def get_book(book_id: int, user: Users = Depends(get_current_user)):
    return await BooksDAO.find_one_or_none(id=book_id)

@router.get("/all")
async def get_all_books(user: Users = Depends(get_current_user)):
    return await BooksDAO.find_all()

@router.post("/add")
async def add_book(book: SBooksModel, user: Users = Depends(get_current_user)):
    return await BooksDAO.create(name=book.name,
                                 author=book.author,
                                 year=book.year,
                                 ISBN=book.ISBN,
                                 quantity=book.quantity,
                                 description=book.description
    )

@router.delete("/{book_id}")
async def delete_book(book_id: int, user: Users = Depends(get_current_user)):
    book = await BooksDAO.find_one_or_none(id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return await BooksDAO.delete_book(id=book_id)

@router.patch("/{book_id}")
async def patch_book(book_id: int, books_data: SBooksModel, user: Users = Depends(get_current_user)):
    book = await BooksDAO.find_one_or_none(id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")


    books_data = books_data.dict(exclude_unset=True)

    return await BooksDAO.update(book_id, books_data)