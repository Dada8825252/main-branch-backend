from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
from controllers import login, auth
from database import get_db
from schemas.user import UserWithToken

login_router = APIRouter()
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token"
)

@login_router.get('/login/github')
async def login_via_github(request: Request):
    return await login.login_via_github(request)

@login_router.get('/auth/github', name='github_login_callback', response_model=UserWithToken)
async def auth_github(request: Request, db: Session = Depends(get_db)):
    return await login.auth_github(request, db)

@login_router.get('/check-user')
async def chekc_user(request: Request):
    user = auth.get_current_user(request)
    return user

@login_router.get('/auth/redirect2otp/{user_id}', name='verify_otp', response_class=HTMLResponse)
async def redirect_to_otp(user_id: int, db: Session = Depends(get_db) ):
    return await login.redirect_to_otp(user_id, db)

@login_router.post('/auth/otp')
async def auth_otp(otp_secret: str = Form(...), otp_input: str = Form(...)):
    return await login.verify_otp(otp_secret, otp_input)