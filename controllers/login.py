from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from authlib.integrations.starlette_client import OAuth
from schemas.user import UserRead
from controllers.user import find_user, create_user
from controllers.token import create_access_token
from controllers.otp import verify_otp
from dotenv import load_dotenv
import os

load_dotenv()

oauth = OAuth()
oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'read:user read:project'},
)

async def login_via_github(request: Request):
    callback_url = request.url_for('github_login_callback')
    return await oauth.github.authorize_redirect(request, callback_url)

async def auth_github(request: Request, db: Session):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get('https://api.github.com/user', token=token)
    profile = user_info.json()

    db_user_auth = find_user(db, 'github', profile["id"])
    if db_user_auth != None:
        user = UserRead.model_validate(db_user_auth.user)
        if user.is_2fa_enabled:
            url = request.url_for('verify_otp',user_id=profile["id"])
            return RedirectResponse(url,status_code=302)
        
        return {"user": user, "access_token": create_access_token(user.model_dump()), "token_type":"Bearer"}
    
    db_user = create_user(db, 'github', profile["id"], profile["login"])
    user = UserRead.model_validate(db_user)

    return {"user": user, "access_token": create_access_token(user.model_dump()), "token_type":"Bearer"}

async def redirect_to_otp(user_id: int, db: Session):
    db_user_auth = find_user(db, 'github', user_id)
    user = UserRead.model_validate(db_user_auth.user)
    otp_secret = user.otp_secret

    if db_user_auth != None:
        return HTMLResponse(content=f"""
        <html>
        <body>
        <form action="/auth/otp" method="POST">
            <input type="hidden" name="otp_secret" value="{otp_secret}">
            <label for="otp">OTP:</label>
            <input type="text" id="otp_input" name="otp_input" required>
            <button type="submit">Submit</button>
        </form>
        </body>
        </html>
    """)
    
async def auth_otp(otp_secret: str, otp_input: str):
    return verify_otp(otp_secret=otp_secret, otp_input=otp_input)