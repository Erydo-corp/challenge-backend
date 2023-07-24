import re
import uuid

from pydantic import BaseModel, validator
from fastapi_users import schemas

from pydantic.networks import EmailStr
from fastapi import HTTPException

LETTER_MATCH_USER = re.compile(r"^[a-zA-ZА-Яа-я\-]+$")


class UserBase(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    second_name: str
    username: str

    @validator("name", "surname", "second_name")
    def validate_name(cls, value):
        if not LETTER_MATCH_USER.match(value):
            raise HTTPException(
                status_code=404, detail="Не корректное имя"
            )
        return value


class User(BaseModel):
    username: str
    name: str
    surname: str
    second_name: str
    email: EmailStr

    class Config:
        orm_mode = True
