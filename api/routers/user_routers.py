from typing import Any

from fastapi import APIRouter, Depends

from api.models.auth import current_user
from api.shemas import user_shems

user_router = APIRouter()


@user_router.get("/protected-route", response_model=user_shems.User)
def protected_route(user: user_shems.User = Depends(current_user)) -> Any:
    return user
