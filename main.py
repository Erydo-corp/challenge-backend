import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.models.auth import auth_backend, fastapi_users
from api.routers.user_routers import user_router
from api.shemas import user_shems

app = FastAPI(title="Challenge")
app_router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app_router.include_router(user_router, prefix="/user", tags=['User'])

app_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=['Auth']
)


app_router.include_router(
    fastapi_users.get_register_router(
        user_schema=user_shems.User,
        user_create_schema=user_shems.UserCreate),
    prefix="/auth",
    tags=['Auth']
)

app.include_router(
    fastapi_users.get_verify_router(user_shems.User),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1")
