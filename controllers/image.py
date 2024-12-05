from pathlib import Path
from fastapi import UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from schemas.image import ImageBase, ImageShow
from models.image import Image

UPLOAD_DIR = Path("images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def upload(db: Session, uploadFile: UploadFile):
    '''
      TODO: Validate file type
    '''
    file_path = UPLOAD_DIR / uploadFile.filename

    if file_path.exists():
        file_path.unlink()

    with open(file_path, "wb") as buffer:
        buffer.write(uploadFile.file.read())
        
    db_image=Image(
        image_path = file_path
    )
    db.add(db_image)
    db.commit()
    return {
        "filename": uploadFile.filename, 
        "message": "File uploaded successfully!"
    }


def read(image_path:str):
    file_path = Path(UPLOAD_DIR) / image_path
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")  
    
    return FileResponse(path=file_path, media_type="image/png")

def update(db: Session, image_path:str, uploadFile: UploadFile):
    file_path = UPLOAD_DIR / image_path
    if file_path.exists():
        file_path.unlink()

    db_image = db.query(Image).filter(Image.image_path == str(file_path)).first()

    new_file_path = UPLOAD_DIR / uploadFile.filename
    with open(new_file_path, "wb") as buffer:
        buffer.write(uploadFile.file.read())

    db_image.image_path = str(new_file_path)
    db.commit()
    return FileResponse(path=new_file_path, media_type="image/png")

def delete(db: Session, image_path:str):
    file_path = UPLOAD_DIR / image_path
    db_image = db.query(Image).filter(Image.image_path == file_path).first()
    
    if db_image == None:
        raise HTTPException(
            status_code=404,
            detail="Image not found."
        )
    db.delete(db_image)
    db.commit()

    if file_path.exists():
        file_path.unlink()

    return {
        "message": "Image deleted successfully"
    }