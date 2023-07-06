from sqlalchemy.ext.asyncio import AsyncSession

from . import user


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db_connection = db

    async def create_user(
            self, name, surname, second_name, email, password
    ) -> user.User:
        new_user = user.User(
            name=name,
            surname=surname,
            second_name=second_name,
            email=email,
            hashed_password=password
        )
        self.db_connection.add(new_user)
        await self.db_connection.flush()
        return new_user
