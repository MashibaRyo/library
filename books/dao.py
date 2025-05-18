from sqlalchemy import delete

from borrowed_books.models import BorrowedBooks
from database import async_session_maker
from books.models import Books
from crud.base import BaseCRUD


class BooksDAO(BaseCRUD):
    model = Books

    @classmethod
    async def delete_book(cls, id):
        async with async_session_maker() as session:

            await session.execute(delete(BorrowedBooks).where(BorrowedBooks.book_id == id))
            await session.execute(delete(Books).where(Books.id == id))

            await session.commit()

            return "Success"
