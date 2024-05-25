from pydantic import BaseModel, Field
from src.schemas.user import UserForImage


class CommentBase(BaseModel):
    comment: str


class CommentResponse(CommentBase):
    id: int
    user: UserForImage

    class Config:
        from_attributes = True