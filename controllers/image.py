from pathlib import Path
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from requests import Session
from schemas.image import ImageBase, ImageShow
from models.image import Image

UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

async def upload(db: Session, file: UploadFile):
    '''
      TODO: Validate file type
    '''
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        buffer.copyfileobj(file.file, buffer)
    db_image=Image(
        image_path = file.filename
    )
    db.add(db_image)
    db.commit()
    return FileResponse(path=file_path, media_type="image/jpeg")

async def read(image_path:str):
    file_path = UPLOAD_DIR / image_path
    if not file_path.exist() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")  
    return FileResponse(path=file_path, media_type="image/jpeg")

async def update(image_path:str, file: UploadFile):
    file_path = UPLOAD_DIR / image_path
    if file_path.exist():
        file_path.unlink()

    new_file_path = UPLOAD_DIR / file.filename
    with open(new_file_path, "wb") as buffer:
        buffer.copyfileobj(file.file, buffer)
    return FileResponse(path=file_path, media_type="image/jpeg")

async def delete(db: Session, image_path:str):
    db_image = db.query(Image).filter(image_path=image_path).first()
    
    if db_image == None:
        raise HTTPException(
            status_code=404,
            detail="Post not found."
        )
    db.delete(db_image)
    db.commit()

    file_path = UPLOAD_DIR / image_path
    if file_path.exist():
        file_path.unlink()

    return {"message": "Image deleted successfully"}