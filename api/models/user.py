import datetime
import uuid

import jwt
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey, UUID, DateTime
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    second_name = Column(String, nullable=False)

    create_at = Column(Date, default=datetime.datetime.now())
    update_at = Column(Date)
    status = Column(Boolean, default=True, comment="Удален пользователь или нет")


class AccessToken(Base):
    __tablename__ = 'access_token'

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, index=True)
    expires = Column(DateTime, default=datetime.datetime.now)
    user_id = Column(UUID, ForeignKey("user.id"))

    user = relationship("User")


