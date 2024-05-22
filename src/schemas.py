from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id: int

    class Config:
        from_attributes = True

class ImageBase(BaseModel):
    image: str = Field(max_length=255)
    description: str = Field(max_length=100)
    qr_code: str = Field(max_length=255)
    user_id: int

class ImageModel(ImageBase):
    tags: List[int]
    comments: List[int]

class ImageUpdate(ImageModel):
    edited_image: str = Field(max_length=255)

class ImageResponse(ImageBase):
    id: int
    tags: List[TagResponse]
    comments: Optional[List[int]] = None

    class Config:
        from_attributes = True