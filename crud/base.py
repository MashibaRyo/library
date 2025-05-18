from sqlalchemy import select, insert, delete, update
from database import async_session_maker


class BaseCRUD:
    model = None

    @classmethod
    async def create(cls, **kwargs):
        async with async_session_maker() as session:
            query = await session.execute(insert(cls.model).values(**kwargs))
            await session.commit()
            return query.scalars()

    @classmethod
    async def find_all(cls, **kwargs):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(**kwargs))

            return query.scalars().all()

    @classmethod
    async def find_password_by_email(cls, email):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model.hashed_password).where(cls.model.email == email))

            return query.scalar()

    @classmethod
    async def find_one_or_none(cls, **kwargs):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(**kwargs))

            return query.scalars().first()


    @classmethod
    async def find_id_by_email(cls, email: str):
        async with async_session_maker() as session:
            query = select(cls.model.id).filter_by(email=email)
            result = await session.execute(query)
            user_id = result.scalar()
            return user_id

    @classmethod
    async def update(cls, data_id: int, data: dict):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == data_id)
                .values(**data)
                .returning(cls.model)
            )

            result = await session.execute(stmt)
            await session.commit()
            return result.scalar_one()
