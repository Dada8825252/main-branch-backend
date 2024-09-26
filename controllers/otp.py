from fastapi import HTTPException
import pyotp
import qrcode

def setup_otp(user_id):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    url = totp.provisioning_uri(name= user_id.to_bytes(4,'big'), issuer_name="SDC_learn")
    
    qr_filename = f"{user_id}_qrcode.png"
    img = qrcode.make(url)
    img.save(qr_filename)
    
    return secret


async def verify_otp(otp_secret: str, otp_input: str):
    totp = pyotp.TOTP(otp_secret)
    if not totp.verify(otp_input):
        raise HTTPException(status_code=400, detail="Invalid OTP")
    return {"message": "login success"}  