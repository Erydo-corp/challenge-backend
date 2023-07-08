from typing import Union
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.shemas import user_shems
from api.models.dals import UserCRUD
from api.config.config_db import get_db

user_router = APIRouter()


async def _create_user(body: user_shems.UserCreate, db) -> user_shems.User:
    async with db as session:
        async with session.begin():
            model_user = UserCRUD(session)
            user = await model_user.create_user(
                name=body.name,
                second_name=body.second_name,
                password=body.password,
                surname=body.surname,
                email=body.email
            )
        return user_shems.User(
            id=user.id,
            name=user.name,
            second_name=user.second_name,
            surname=user.surname,
            email=user.email
        )


async def _delete_user(id, db) -> Union[user_shems.User]:
    pass


@user_router.post("/", response_model=user_shems.User)
async def create_user(body: user_shems.UserCreate, db: AsyncSession = Depends(get_db)) -> user_shems.User:
    return await _create_user(body, db)