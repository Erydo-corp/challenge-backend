import datetime
import hashlib
import random
import string
from typing import Union
from uuid import UUID

import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, and_, select
from fastapi.exceptions import HTTPException

from api.shemas.user_shems import UserCreate
from api.config import settings
from . import user


def get_random_string(length=12):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


class UserCRUD:
    def __init__(self, db: AsyncSession):
        self.db_connection = db

    async def create_user(self, user_shem: UserCreate) -> user.User:
        password = hash_password(user_shem.password, user_shem.email)
        new_user = user.User(name=user_shem.name,
                        surname=user_shem.surname,
                        second_name=user_shem.second_name,
                        email=user_shem.email,
                        hashed_password=f'{user_shem.email}${password}'
                        )
        self.db_connection.add(new_user)
        await self.db_connection.flush()
        token = AccessTokenCRUD.create_auth_token(new_user)
        self.db_connection.add(token)
        return token

    async def get_user(self, email: str):
        users = select(user.User).where(user.User.email == email)
        result = await self.db_connection.execute(users)
        res = result.fetchone()
        if res is None:
            raise HTTPException(
                status_code=400,
                detail="Не найден, пользователь"
            )

        return res[0]

    async def user_id(self, user_id: str):
        result = await self.db_connection.execute(
            select(user.User).where(user.User.id == user_id)
        )
        res = result.fetchone()
        if res is None:
            return res[0]

    async def delete_user(self, id: UUID) -> Union[UUID, None]:
        query = update(user.User). \
            where(and_(id, user.User.is_active == True)). \
            values(is_active=False). \
            returning(user.User.id)
        result = await self.db_connection.execute(query)
        delete_user = result.fetchone()
        if delete_user is not None:
            return delete_user[0]


class AccessTokenCRUD:
    def __init__(self, db: AsyncSession):
        self.db_connection = db
        self.user = UserCRUD(db)

    async def find_user(self, email: str):
        user_id = await self.user.get_user(email)
        token = await self.db_connection.execute(
            select(user.AccessToken).where(user.AccessToken.user_id == user_id.id))
        res = token.fetchone()
        if res is not None:
            return res[0]

    async def auth_user(self, username, password):
        acces = AccessTokenCRUD(self.db_connection)
        user = self.user
        res = await user.get_user(username)
        pas = validate_password(password, res.hashed_password)

        if pas:
            token = await acces.find_user(username)
            return token
        else:
            raise HTTPException(
                status_code=403,
                detail="Неверный пароль"
            )

    @staticmethod
    def create_auth_token(users: UserCreate):
        delta = datetime.datetime.utcnow() + datetime.timedelta(days=14)
        return user.AccessToken(
            user_id=users.id,
            token=jwt.encode(
                {
                    "sub": users.email,
                    "exp": delta
                },
                settings.SECRET_KEY))
