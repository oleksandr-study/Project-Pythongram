from fastapi import APIRouter, HTTPException
from cloudinary.utils import cloudinary_url

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
    angle: int = None
):
    try:
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

        url, options = cloudinary_url(public_id, **transformations)
        return {"url": url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))