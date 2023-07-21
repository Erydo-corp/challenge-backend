import hashlib
import random
import string
from typing import Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_
from sqlalchemy.orm import Session
from api.shemas.user_shems import UserCreate

from . import user


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db_connection = db

    async def create_user(self, user_shem: UserCreate) -> user.User:
        salt = get_random_string()
        password = hash_password(user_shem.password, salt)
        new_user = user.User(
            name=user_shem.name,
            surname=user_shem.surname,
            second_name=user_shem.second_name,
            email=user_shem.email,
            hashed_password=f'{salt}${password}'
        )
        self.db_connection.add(new_user)
        token = user.AccessToken(user_id=new_user.id)
        self.db_connection.add(token)
        await self.db_connection.flush()
        return token

    async def get_user(self, email: str, db: Session):
        return db.query(user.User).where(user.User.email == email).first()

    async def delete_user(self, id: UUID) -> Union[UUID, None]:
        query = update(user.User).\
            where(and_(id, user.User.is_active == True)).\
            values(is_active=False).\
            returning(user.User.id)
        result = await self.db_connection.execute(query)
        delete_user = result.fetchone()
        if delete_user is not None:
            return delete_user[0]


class AccessTokenCRUD:
    def __init__(self, db: AsyncSession):
        self.db_connection = db


