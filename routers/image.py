from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from schemas.image import ImageBase, ImageShow
from pydantic import PositiveInt
from controllers import image
from database import get_db

image_router = APIRouter()

@image_router.post('/')
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return image.upload(db=db, uploadFile=file)

@image_router.get('/{image_path}')
def read_image(image_path: str):
    return image.read(image_path=image_path)

@image_router.put('/{image_path}')
def update_image(image_path: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return image.update(db=db, image_path=image_path, uploadFile=file)

@image_router.delete('/{image_path}')
def delete_image(image_path: str, db: Session = Depends(get_db)):
    return image.delete(db=db, image_path=image_path)