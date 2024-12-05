from sqlalchemy.orm import Session
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse,RedirectResponse
from authlib.integrations.starlette_client import OAuth
from schemas.user import UserRead
from controllers.user import find_user, create_user
from controllers.token import create_access_token
from controllers.otp import verify_otp
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()

MAX_FAIL_ATTEMPTS = 5
LOCKOUT_DURATION = timedelta(minutes=10)

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
            return RedirectResponse(url=f"/auth/redirect2otp/{profile['id']}", status_code=302)
        
        return {
            "user": user, 
            "access_token": create_access_token(user.model_dump()), 
            "token_type":"Bearer"
        }
    
    db_user = create_user(db, 'github', profile["id"], profile["login"])
    user = UserRead.model_validate(db_user)

    return {"user": user, "access_token": create_access_token(user.model_dump()), "token_type":"Bearer"}

async def redirect_to_otp(profile_id: int, db: Session):
    form_action_url = f"/auth/otp/{profile_id}"
    
    return HTMLResponse(content=f"""
        <html>
        <body>
        <form action="{form_action_url}" method="POST">
            <label for="otp">OTP:</label>
            <input type="text" id="otp_input" name="otp_input" required>
            <button type="submit">Submit</button>
        </form>
        </body>
        </html>
    """)
    
async def auth_otp(profile_id: int, otp_input: str, db: Session):
    db_user_auth = find_user(db, 'github', profile_id)
    if not db_user_auth:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = UserRead.model_validate(db_user_auth.user)
    otp_secret = user.otp_secret

    if db_user_auth.login_fail_time >= MAX_FAIL_ATTEMPTS:
        if db_user_auth.updated_at and datetime.now() < db_user_auth.updated_at + LOCKOUT_DURATION:
            raise HTTPException(
                status_code=429,
                detail=f"Too many failed attempts. Please try again after {db_user_auth.updated_at + LOCKOUT_DURATION - datetime.now()}."
            )
    
    is_valid = await verify_otp(otp_secret, otp_input)
    if not is_valid:
        db_user_auth.login_fail_time += 1
        db_user_auth.updated_at = datetime.now()  # Update the timestamp
        db.commit()

        if db_user_auth.login_fail_time >= MAX_FAIL_ATTEMPTS:
            raise HTTPException(
                status_code=429,
                detail=f"Too many failed attempts. Locked out for {LOCKOUT_DURATION}."
            )
        
        redirect_url = f"/auth/redirect2otp/{profile_id}"
        response = RedirectResponse(url=redirect_url, status_code=303)
        return response
    
    db_user_auth.login_fail_time = 0
    db_user_auth.updated_at = datetime.now()
    db.commit()
    return {
        "user": user,
        "access_token": create_access_token(user.model_dump()),
        "token_type": "Bearer"
    } 