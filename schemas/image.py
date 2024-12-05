from fastapi import UploadFile
from pydantic import BaseModel, PositiveInt


class ImageBase(BaseModel):
    image_path: str 

class ImageShow(ImageBase):
    content: UploadFile