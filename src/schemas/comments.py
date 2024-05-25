from pydantic import BaseModel, Field
from src.schemas.images import UserForImage


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