from datetime import timedelta
from typing import Union, Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.shemas import user_shems
from api.models.dals import UserCRUD, AccessTokenCRUD
from api.config.config_db import get_db

user_router = APIRouter()


async def _create_user(body: user_shems.UserCreate, db: AsyncSession) -> user_shems.TokenBase:
    model_user = UserCRUD(db)
    user = await model_user.create_user(body)
    await db.commit()
    return user


async def _delete_user(id, db) -> Union[user_shems.User]:
    pass


@user_router.post("/")
async def create_user(body: user_shems.UserCreate, db: AsyncSession = Depends(get_db)):
    return await _create_user(body, db)


@user_router.post("/auth")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db)):
    user = AccessTokenCRUD(db)
    valid = await user.auth_user(form_data.username, form_data.password)
    return valid
