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


router = APIRouter(tags=["images"])

cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )


@router.get("/images", response_model=List[ImageResponse])
async def get_all_images(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves all images with optional pagination.

    :param skip: The number of images to skip.
    :type skip: int
    :param limit: The maximum number of images to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :return: A list of images.
    :rtype: List[ImageResponse]
    """
    images = await repository_images.get_all_images(skip, limit, db)
    return images


@router.get("/images/user/{user_id}", response_model=List[ImageResponse])
async def get_images_by_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all images for a specific user.

    :param user_id: The ID of the user.
    :type user_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of images for the specified user.
    :rtype: List[ImageResponse]
    """

    images = await repository_images.get_images_by_user(user_id, db)
    if images is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return images


@router.get("/images/{image_id}", response_model=List[ImageResponse])
async def get_images_by_id(image_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    """
    Retrieves a specific image by ID.

    :param image_id: The ID of the image.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The image with the specified ID.
    :rtype: ImageResponse
    """
    image = await repository_images.get_images_by_id(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" Image NOT FOUND")
    return image


@router.post("/images", response_model=ImageResponse, status_code=status.HTTP_201_CREATED)
async def create_image(
        image: UploadFile = File(),
        description: str | None = Form(None, description="Add description to your image"),
        tags: str | None = Form(None, description="Add tags to your image"),
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)
        ):
    """
    Creates a new image with a description and tags.

    :param image: The uploaded image file.
    :type image: UploadFile
    :param description: The description of the image.
    :type description: str
    :param tags: The tags associated with the image.
    :type tags: str
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The newly created image.
    :rtype: ImageResponse
    """
    image = await repository_images.create_image(image, description, current_user, tags, db)
    return image


@router.put("/images/{image_id}", response_model=ImageResponse)
async def update_image(body: ImageUpdateSchema, image_id: int, db: Session = Depends(get_db),
                       # current_user: User = Depends(auth_service.get_current_user)
                       ):
    """
    Updates an existing image by ID.

    :param body: The updated data for the image.
    :type body: ImageUpdateSchema
    :param image_id: The ID of the image to update.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The updated image.
    :rtype: ImageResponse
    """
    current_user = db.query(User).filter(User.id == 3).first()
    image = await repository_images.update_image(image_id, body, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image


@router.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_image(image_id: int, db: Session = Depends(get_db),
                       #current_user: User = Depends(auth_service.get_current_user)
                       ):
    """
    Removes an image by ID.

    :param image_id: The ID of the image to remove.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The current authenticated user.
    :type current_user: User
    :return: The removed image.
    :rtype: ImageResponse
    """
    current_user = db.query(User).filter(User.id == 3).first()
    image = await repository_images.remove_image(image_id, current_user, db)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    return image