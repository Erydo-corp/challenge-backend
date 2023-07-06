from fastapi import APIRouter

from app.shemas import user_shems
from app.models.crud import UserCRUD
from app.config.config_db import async_session

user_router = APIRouter()


async def _create_user(body: user_shems.UserCreate) -> user_shems.User:
    async with async_session() as session:
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


@user_router.post("/", response_model=user_shems.User)
async def create_user(body: user_shems.UserCreate) -> user_shems.User:
    return await _create_user(body)