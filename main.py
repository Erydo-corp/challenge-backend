import uvicorn
from typing import Annotated

from fastapi import FastAPI, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.oauth2 import OAuth2PasswordBearer
from api.routers.user_routers import user_router

app = FastAPI(title="Challenge")

oauth = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app_router = APIRouter()
app_router.include_router(user_router, prefix="/user", tags=['User'])


app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1")
