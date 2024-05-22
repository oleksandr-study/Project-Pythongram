from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session



from src.models.models import Image, User

def get_all_images(skip: int, limit: int, db: Session) -> List[Image]:
    return db.query(Image).offset(skip).limit(limit).all()

def get_images_by_user(user_id: int, db: Session) -> List[Image]:
    user = db.query(User).filter(User.id == user_id).first()
    return db.query(Image).filter(Image.user_id == user.id).all()

def get_images_by_id(image_id: int, db: Session) -> Image:
    return db.query(Image).filter(Image.id == image_id).all()


