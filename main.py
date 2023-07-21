import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.routers.user_routers import user_router

app = FastAPI(title="Challenge")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app_router = APIRouter()


@app.get("/")
def index():
    return "Hello"


app_router.include_router(user_router, prefix="/user", tags=['User'])


app.include_router(app_router)

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1")
