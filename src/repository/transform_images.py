import cloudinary
import qrcode

from typing import Dict, Optional
from fastapi import HTTPException, status
from pathlib import Path
from sqlalchemy.orm import Session
from cloudinary.utils import cloudinary_url
from src.conf.config import cloudinary_start
from cloudinary.uploader import upload
from sqlalchemy.orm import Session
from src.models.models import Image


def make_qr_code(edited_image_url: Path, image_id: int, db: Session):
    """
    The make_qr_code function takes in the edited image url and the image id.
    It then creates a QR code using qrcode, saves it as a png file, uploads it to cloudinary
    and returns its secure url.
    
    :param edited_image_url: Path: Pass the path of the edited image to the function
    :param image_id: int: Name the qr code file
    :param db: Session: Pass in the database session to the function
    :return: A dictionary, which is not a valid url
    :doc-author: Trelent
    """
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data('Some data')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    qr_code_file = "qr_code.png"
    img.save(qr_code_file)

    cloudinary_start()
    upload_qr_code = cloudinary.uploader.upload(
        qr_code_file,
        public_id=f"Qr_Code/qr_code_{image_id}",
        overwrite=True,
        invalidate=True,
    )

    return upload_qr_code["secure_url"]


async def transform_image_url(
    public_id: str,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: Optional[str] = None,
    gravity: Optional[str] = None,
    quality: Optional[str] = None,
    fetch_format: Optional[str] = None,
    effect: Optional[str] = None,
    angle: Optional[int] = None,
    db: Session = None
) -> str:
    """
    Transforms the image with the specified parameters and updates the edited image URL in the database.

    Parameters:
    - public_id (str): The public ID of the image in Cloudinary.
    - width (Optional[int]): The desired width of the transformed image.
    - height (Optional[int]): The desired height of the transformed image.
    - crop (Optional[str]): The crop mode for the image transformation.
    - gravity (Optional[str]): The gravity setting for the transformation.
    - quality (Optional[str]): The quality setting for the transformation.
    - fetch_format (Optional[str]): The fetch format for the transformed image.
    - effect (Optional[str]): The effect to apply to the transformed image.
    - angle (Optional[int]): The angle of rotation for the transformation.
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
        "angle": angle
    }

    transformations = {k: v for k, v in transformations.items() if v is not None}

    url, options = cloudinary_url(public_id, **transformations)
    
    upload_result = upload(url)

    if 'url' not in upload_result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to upload image to Cloudinary")
    
    image = db.query(Image).filter(Image.public_id == public_id).first()
    if not image:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    
    image.edited_image = upload_result['url']
    db.commit()
    db.refresh(image)
    
    return image.edited_image

async def update_image(image_id: int, edited_image_url: str, db: Session, user_id: int) -> Image:
    """
    Updates the edited image URL of an existing image.

    Parameters:
    - image_id (int): The ID of the image to update.
    - edited_image_url (str): The new edited image URL.
    - db (Session): The SQLAlchemy session object.
    - user_id (int): The ID of the user who owns the image.

    Returns:
    - Image: The updated image object, or None if not found.
    """
    image = db.query(Image).filter(Image.id == image_id, Image.user_id == user_id).first()
    if image:
        image.edited_image = edited_image_url
        db.commit()
        db.refresh(image)
    return image