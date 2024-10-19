from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from schemas.image import ImageBase, ImageShow
from pydantic import PositiveInt
from controllers import image
from database import get_db

image_router = APIRouter

@image_router.post('', response_model=FileResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    image.upload(db=db, file=file)

@image_router.get('/{image_path}', response_model=FileResponse)
async def read_image(image_path: str):
    image.read(image_path=image_path)

@image_router.put('/{image_path}', response_model=FileResponse)
async def update_image(image_path: str, file: UploadFile = File(...)):
    image.update(image_path=image_path, file=file)

@image_router.delete('/{image_path}')
async def delete_image(image_path: str, db: Session = Depends(get_db)):
    image.delete(db=db, image_path=image_path)