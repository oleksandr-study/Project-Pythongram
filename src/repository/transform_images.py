import cloudinary
import cloudinary.uploader
import qrcode

from typing import Dict
from fastapi import HTTPException
from pathlib import Path
from sqlalchemy.orm import Session
from cloudinary.utils import cloudinary_url

from src.conf.config import cloudinary_start


def make_qr_code(edited_image_url: Path, image_id: int, db: Session):
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


async def get_transformed_image_url(public_id: str, transformations: Dict) -> str:
    """
    Returns the URL of the transformed image using Cloudinary.

    :param public_id: The public ID of the image in Cloudinary
    :param transformations: A dictionary of transformation parameters
    :return: URL of the transformed image
    :raises HTTPException: If there is an error during transformation
    """
    try:
        url, options = cloudinary_url(public_id, **transformations)
        return url
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
