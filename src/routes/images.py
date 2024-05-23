from typing import List


from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status
from src.database.db import get_db
#from src.database.models import User
#from src.schemas import ContactModel, ContactResponse
from src.repository import images as repository_images
#from src.services.auth import auth_service
from src.schemas.schemas import ImageResponse, ImageModel, ImageUpdate

router = APIRouter(tags=["images"])

@router.get("/images", response_model=List[ImageResponse])
async def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = repository_images.get_all_images(skip, limit, db)
    return await images

@router.get("/users/{user_id}", response_model=List[ImageResponse])
async def get_images_by_user(user_id: int, db: Session = Depends(get_db)):
    images = repository_images.get_images_by_user(user_id, db)
    return await images

@router.get("/images/{image_id}", response_model=List[ImageResponse])
async def get_images_by_id(image_id: int, db: Session = Depends(get_db)):
    image = repository_images.get_images_by_id(image_id, db)
    return await image

@router.post("/images", response_model=ImageResponse)
async def create_image(body: ImageModel, db: Session = Depends(get_db),
                      #current_user: User = Depends(auth_service.get_current_user)
                       ):
    return await repository_images.create_image(body,
                                                #current_user,
                                        db)

@router.put("/{image_id}", response_model=ImageResponse)
async def update_image(body: ImageUpdate, image_id: int, db: Session = Depends(get_db), current_user: int=1):
    image = await repository_images.update_image(image_id, body, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.delete("/{image_id}", response_model=ImageResponse)
async def remove_image(image_id: int, db: Session = Depends(get_db), current_user: int=1):
    image = await repository_images.remove_image(image_id, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image
