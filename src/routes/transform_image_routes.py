from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session
from src.repository.transform_images import get_transformed_image_url
from src.database.db import get_db

router = APIRouter()

@router.get("/transform-image/")
async def transform_image(
    public_id: str,
    width: int = None,
    height: int = None,
    crop: str = None,
    gravity: str = None,
    quality: str = None,
    fetch_format: str = None,
    effect: str = None,
    angle: int = None,
    db: Session = Depends(get_db)
):
    """
    Transform an image using various parameters.

    :param public_id: The public ID of the image in Cloudinary
    :param width: The width to resize the image to
    :param height: The height to resize the image to
    :param crop: The cropping method
    :param gravity: The gravity for cropping
    :param quality: The quality of the image
    :param fetch_format: The format to fetch the image in
    :param effect: The effect to apply to the image
    :param angle: The angle to rotate the image
    :param db: The database session
    :return: A dictionary containing the URL of the transformed image
    :raises HTTPException: If there is an error during transformation
    """
    transformations = {}
    if width:
        transformations['width'] = width
    if height:
        transformations['height'] = height
    if crop:
        transformations['crop'] = crop
    if gravity:
        transformations['gravity'] = gravity
    if quality:
        transformations['quality'] = quality
    if fetch_format:
        transformations['fetch_format'] = fetch_format
    if effect:
        transformations['effect'] = effect
    if angle:
        transformations['angle'] = angle

    try:
        url = await get_transformed_image_url(public_id, transformations)
        return {"url": url}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
