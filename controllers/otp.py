from fastapi import HTTPException
import pyotp
import qrcode
import os

def setup_otp(user_id):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    url = totp.provisioning_uri(name=str(user_id), issuer_name="SDC_learn")
    
    qr_filename = f"{user_id}_qrcode.png"
    img = qrcode.make(url)    

    upload_dir = "./qrcodes"
    os.makedirs(upload_dir, exist_ok=True)  # Ensure directory exists
    qr_filepath = os.path.join(upload_dir, qr_filename)
    img.save(qr_filepath)

    return secret


async def verify_otp(otp_secret: str, otp_input: str):
    totp = pyotp.TOTP(otp_secret)
    return totp.verify(otp_input)