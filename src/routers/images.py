from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
#from src.database.models import User
#from src.schemas import ContactModel, ContactResponse
from src.repository import images as repository_images
#from src.services.auth import auth_service
from src.models.models import User
from src.schemas import ImageResponse

router = APIRouter(tags=["images"])

@router.get("/images", response_model=List[ImageResponse])
def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = repository_images.get_all_images(skip, limit, db)
    return images

@router.get("/users/{user_id}", response_model=List[ImageResponse])
def get_images_by_user(user_id: int, db: Session = Depends(get_db)):
    images = repository_images.get_images_by_user(user_id, db)
    return images

@router.get("/images/{image_id}", response_model=List[ImageResponse])
def get_images_by_id(image_id: int, db: Session = Depends(get_db)):
    image = repository_images.get_images_by_id(image_id, db)
    return image
