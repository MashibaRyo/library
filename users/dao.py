from fastapi import HTTPException
from sqlalchemy import delete
from starlette import status

from borrowed_books.models import BorrowedBooks
from crud.base import BaseCRUD
from database import async_session_maker
from users.models import Users


class UsersDAO(BaseCRUD):
    model = Users

    @classmethod
    async def delete_user(cls, user_id):
        async with async_session_maker() as session:
            user = await UsersDAO.find_one_or_none(id=user_id)

            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

            await session.execute(delete(BorrowedBooks).where(BorrowedBooks.reader_id == user_id))
            await session.execute(delete(Users).where(Users.id == user_id))

            await session.commit()
