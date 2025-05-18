from fastapi import APIRouter, Depends

from borrowed_books.dao import BorrowedBooksDAO
from borrowed_books.shemas import SBorrowedBooksModel, SBorrowedBooksReturnModel
from users.dependencies import get_current_user
from users.shemas import User

router = APIRouter(
    prefix="/borrowed_books",
    tags=["borrowed_books"]
)


@router.get("")
async def get_borrowed_books(current_user: User = Depends(get_current_user)):
    return await BorrowedBooksDAO.find_all(reader_id=current_user.id)

@router.get("/{id}")
async def get_borrowed_book(id: int):
    return await BorrowedBooksDAO.find_one_or_none(id=id)

@router.post("/add")
async def add_borrowed_book(borrowed: SBorrowedBooksModel, current_user: User = Depends(get_current_user)):
    borrowed = borrowed.dict()

    borrowed.update({"reader_id": current_user.id})

    return await BorrowedBooksDAO.create_borrowed(borrowed)

@router.post("/return_book")
async def return_book(borrowed: SBorrowedBooksReturnModel,  current_user: User = Depends(get_current_user)):
    borrowed = borrowed.dict()

    borrowed.update({"reader_id": current_user.id})

    return await BorrowedBooksDAO.return_borrowed(borrowed)
