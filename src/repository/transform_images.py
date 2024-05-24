from typing import Dict
from fastapi import HTTPException
from cloudinary.utils import cloudinary_url

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
