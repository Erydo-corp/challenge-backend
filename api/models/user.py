import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Boolean, Date
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

Base = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    second_name = Column(String, nullable=False)

    create_at = Column(Date, default=datetime.datetime.now())
    update_at = Column(Date)

