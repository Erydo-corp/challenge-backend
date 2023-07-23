import re
import uuid
from typing import Optional, Any

from pydantic import BaseModel, validator, UUID4
from fastapi_users import schemas
from pydantic.fields import Field
from pydantic.networks import EmailStr
from fastapi import HTTPException
from pydantic.schema import datetime

LETTER_MATCH_USER = re.compile(r"^[a-zA-ZА-Яа-я\-]+$")


class TrendsModel(BaseModel):
    class Config:
        orm_model = True


class UserBase(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    second_name: str
    password: str

    @validator("name", "surname", "second_name")
    def validate_name(cls, value):
        if not LETTER_MATCH_USER.match(value):
            raise HTTPException(
                status_code=404, detail="Не корректное имя"
            )
        return value


class TokenBase(BaseModel):
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class User(UserBase):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    second_name: str
    token: TokenBase = {}


class UserEmail(BaseModel):
    email: EmailStr