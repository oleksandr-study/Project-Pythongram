from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional

from src.database.db import get_db
from src.repository.transform_images import transform_image_url, update_image
from src.models.models import Image, User
from src.services.auth import auth_service

router = APIRouter()

@router.post("/transform")
async def transform_image(
    image_id: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: Optional[str] = None,
    gravity: Optional[str] = None,
    quality: Optional[str] = None,
    fetch_format: Optional[str] = None,
    effect: Optional[str] = None,
    angle: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user)
):
    """
    Transform an image using Cloudinary and update the edited image URL in the database.

    Parameters:
    - public_id (str): The public ID of the image in Cloudinary.
    - width (int, optional): The width to resize the image to.
    - height (int, optional): The height to resize the image to.
    - crop (str, optional): The crop mode for the image transformation.
    - gravity (str, optional): The gravity mode for the image transformation.
    - quality (str, optional): The quality setting for the image transformation.
    - fetch_format (str, optional): The fetch format for the image transformation.
    - effect (str, optional): The effect to apply to the image.
    - angle (int, optional): The angle to rotate the image.
    - db (Session): The SQLAlchemy session object.

    Returns:
    - str: The URL of the transformed image.

    Raises:
    - HTTPException: If the image is not found in the database or if the image upload to Cloudinary fails.
    """
    transformations = {
        "width": width,
        "height": height,
        "crop": crop,
        "gravity": gravity,
        "quality": quality,
        "fetch_format": fetch_format,
        "effect": effect,
        "angle": angle,
    }

    # Remove None values from the transformations dictionary
    transformations = {k: v for k, v in transformations.items() if v is not None}

    transformed_url = await transform_image_url(image_id, db, current_user, **transformations)

    return {"transformed_url": transformed_url}


@router.put("/update/{image_id}")
async def edit_image(image_id: int, edited_image_url: str, user_id: int, db: Session = Depends(get_db)):
    """
    Update the edited image URL of an existing image.

    Parameters:
    - image_id (int): The ID of the image to update.
    - edited_image_url (str): The new edited image URL.
    - user_id (int): The ID of the user who owns the image.
    - db (Session): The SQLAlchemy session object.

    Returns:
    - Image: The updated image object, or None if not found.
    """
    updated_image = await update_image(image_id, edited_image_url, db, user_id)
    if updated_image:
        return {"message": "Image updated successfully.", "image": updated_image}
    else:
        raise HTTPException(status_code=404, detail="Image not found or not authorized.")
