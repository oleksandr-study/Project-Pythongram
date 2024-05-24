from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class UserForImage(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    comment: str

class CommentResponse(CommentBase):
    id: int
    user: UserForImage

    class Config:
        from_attributes = True


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
    tags: List[str]
    user_id: int
    #user: UserForImage | None

class ImageModel(ImageBase):
    comments: Optional[List[CommentResponse]]

class ImageUpdateSchema(BaseModel):
    description: str = Field(max_length=100)
    qr_code: str = Field(max_length=255)
    edited_image: str = Field(max_length=255)
    tags: List[int]
    comments: Optional[List[int]]

    class Config:
        from_attributes = True

class ImageResponse(ImageBase):
    id: int
    #user: UserForImage
    user_id: int
    tags: List[TagResponse]
    comments: Optional[List[CommentResponse]]

    class Config:
        from_attributes = True

