from sqlalchemy import select, insert, update, exists, and_
from sqlalchemy.sql.functions import func

from books.models import Books
from borrowed_books.models import BorrowedBooks
from borrowed_books.shemas import SBorrowedBooksModel
from crud.base import BaseCRUD
from database import async_session_maker
from users.models import Users


class BorrowedBooksDAO(BaseCRUD):
    model = BorrowedBooks

    @classmethod
    async def create_borrowed(cls, data: dict):
        async with async_session_maker() as session:
            exists_query = await session.execute(
                select(
                    exists().where(and_(
                        Users.id == data['reader_id'],
                        Books.id == data['book_id']
                    ))
                )
            )
            if not exists_query.scalar():
                return "Не найдено"

            quantity = await session.execute(
                select(Books.quantity)
                .where(Books.id == data['book_id'])
            )

            if quantity.scalar() < 1:
                 return "Книг нет"
            count_query = await session.execute(
                select(func.count(BorrowedBooks.id))
                .where(
                    BorrowedBooks.reader_id == data['reader_id'],
                    BorrowedBooks.return_date.is_(None)
                )
            )
            if count_query.scalar() >= 3:
                return "Количество книг у одного читателя > 3"

            await session.execute(insert(BorrowedBooks).values(data))

            await session.execute(update(Books)
                                  .where(Books.id == data['book_id'])
                                  .values(quantity=Books.quantity-1))

            await session.commit()

            return "Success"

    @classmethod
    async def return_borrowed(cls, data: dict):
        async with async_session_maker() as session:
            exists_query = await session.execute(
                select(
                    exists().where(and_(
                        Users.id == data['reader_id'],
                        Books.id == data['book_id']
                    ))
                )
            )
            if not exists_query.scalar():
                return "Не найдено"

            is_return = await session.execute(
                select(BorrowedBooks.return_date)
                .where(BorrowedBooks.book_id == data['book_id'],
                BorrowedBooks.reader_id == data['reader_id'])
            )

            if is_return.scalar():
                return "Книга уже возвращена"


            await session.execute(
                update(BorrowedBooks)
                .where(BorrowedBooks.book_id == data['book_id'],
                BorrowedBooks.reader_id == data['reader_id'])
                .values(return_date=data['return_date'])
            )

            await session.execute(
                update(Books)
                .where(Books.id == data['book_id'])
                .values(quantity=Books.quantity+1)
            )

            await session.commit()

            return "Success"