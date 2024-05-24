from typing import List

import cloudinary
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File, Form

from src.conf.config import settings
from src.database.db import get_db
from src.models.models import User
from src.repository import images as repository_images
from src.schemas.images import ImageResponse, ImageUpdateSchema
from src.services.auth import auth_service
from src.repository import comments as repository_comments


router = APIRouter(tags=["images"])

cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )


@router.get("/images", response_model=List[ImageResponse])
async def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    images = await repository_images.get_all_images(skip, limit, db)
    return images


@router.get("/users/{user_id}", response_model=List[ImageResponse])
async def get_images_by_user(user_id: int, db: Session = Depends(get_db)):
    images = await repository_images.get_images_by_user(user_id, db)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return images


@router.get("/images/{image_id}", response_model=List[ImageResponse])
async def get_images_by_id(image_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    image = await repository_images.get_images_by_id(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return image


@router.post("/images", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
        image: UploadFile = File(),
        description: str = Form(),
        tags: str = Form(),
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
        ):

    public_id = f"PhotoShare/{current_user.id}"
    res = cloudinary.uploader.upload(image.file, public_id=public_id, overwrite=True)
    image = await repository_images.create_image(res['url'], description, current_user, tags, db)
    return image


@router.put("/images/{image_id}", response_model=ImageResponse)
async def update_image(body: ImageUpdateSchema, image_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    image = await repository_images.update_image(image_id, body, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_image(image_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    image = await repository_images.remove_image(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.post("/images/{image_id}/comments", response_model=List[CommentResponse])
async def create_comment(image_id: int,body: CommentBase ,db: Session = Depends(get_db)):
    image = repository_images.get_images_by_id(image_id, db)
    if image:
        comment = repository_comments.create_comment(image_id,db,comment=body,user_id=1)
    return await comment

