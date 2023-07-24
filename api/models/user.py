import datetime

from fastapi import Depends
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, TIMESTAMP, Integer, ForeignKey, UUID, DateTime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from api.config.config_db import get_db

Base = declarative_base()


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    username = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    second_name = Column(String, nullable=False)

    create_at = Column(TIMESTAMP, default=datetime.datetime.now())
    update_at = Column(TIMESTAMP)
    status = Column(Boolean, default=True, comment="Удален пользователь или нет")




