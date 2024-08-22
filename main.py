from fastapi import FastAPI, APIRouter, Request
from routers.post import post_router
from routers.login import login_router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

router = APIRouter()
router.include_router(
    post_router,
    prefix='/posts'
)
router.include_router(
    login_router
)
app.include_router(router)

app.add_middleware(SessionMiddleware, secret_key=os.getenv('APP_SECRET'))