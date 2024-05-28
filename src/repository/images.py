from typing import List

import cloudinary
import uuid

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from src.models.models import Image, User, Tag, Role
from src.schemas.images import ImageUpdateSchema
from cloudinary.utils import cloudinary_url



async def get_all_images(skip: int, limit: int, db: Session) -> List[Image]:
    """
    Retrieves a list of all images with specified pagination parameters.

    :param skip: The number of images to skip.
    :type skip: int
    :param limit: The maximum number of images to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :return: A list of images.
    :rtype: List[Image]
    """
    return db.query(Image).offset(skip).limit(limit).all()


async def get_images_by_user(user_id: int, db: Session) -> List[Image]:
    """
    Retrieves a list of images for a specific user.

    :param user_id: The ID of the user to retrieve images for.
    :type user_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of images belonging to the user.
    :rtype: List[Image]
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User NOT FOUND")

    return db.query(Image).filter(Image.user_id == user.id).all()


async def get_images_by_id(image_id: int, user: User, db: Session) -> Image:
    """
    Retrieves a single image with the specified ID for a specific user.

    :param image_id: The ID of the image to retrieve.
    :type image_id: int
    :param user: The user to retrieve the image for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The image with the specified ID, or None if it does not exist.
    :rtype: Image | None
    """
    return db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).all()


async def create_image(image, description, user: User, all_tags: str|None, db: Session) -> Image:
    """
    Creates a new image for a specific user with provided tags and description.

    :param image_url: The URL of the image.
    :type image_url: str
    :param description: The description of the image.
    :type description: str
    :param user: The user to create the image for.
    :type user: User
    :param all_tags: A comma-separated string of tag names.
    :type all_tags: str
    :param db: The database session.
    :type db: Session
    :return: The newly created image.
    :rtype: Image
    :raises HTTPException: If more than 5 tags are provided.
    """
    tags = []
    if all_tags:
        list_tags = all_tags.split(", ")
        if len(list_tags) > 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can add up to 5 tags only.")

        for tag_name in list_tags:
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()
            tags.append(tag)
    im_uuid = uuid.uuid4()
    public_id = f"{im_uuid}"
    url, ot = cloudinary_url(public_id)
    image_url = cloudinary.uploader.upload(image.file, public_id=public_id, url = url, overwrite=True)
    image = Image(
        image=image_url['url'],
        user_id=user.id,
        description=description,
        tags=tags
    )

    db.add(image)
    db.commit()
    db.refresh(image)
    return image


async def remove_image(image_id: int, user: User, db: Session) -> Image | None:
    """
    Removes a single image with the specified ID. If the user is an admin, any image can be removed;
    otherwise, only images belonging to the user can be removed.

    :param image_id: The ID of the image to remove.
    :type image_id: int
    :param user: The user attempting to remove the image.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The removed image, or None if it does not exist.
    :rtype: Image | None
    """
    if user.role == Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()


    if image:
        public_id = image.image.split("/")[-1].split(".")[0]
        print(f'1 {public_id}')
        cloudinary.uploader.destroy(public_id)
        if image.edited_image:
            public_id = image.image.split("/")[-1].split(".")[0]
            print(f'2 {public_id}')
            cloudinary.uploader.destroy(public_id)
        if image.qr_code:
            public_id = image.qr_code.split("/")[-1].split(".")[0]
            print(f'3 {public_id}')
            cloudinary.uploader.destroy(public_id)
        db.delete(image)
        db.commit()
    return image


async def update_image(image_id: int, body: ImageUpdateSchema, user: User, db: Session) -> Image | None:
    """
    Updates a single image with the specified ID for a specific user, including updating the tags.

    :param image_id: The ID of the image to update.
    :type image_id: int
    :param body: The updated data for the image.
    :type body: ImageUpdateSchema
    :param user: The user attempting to update the image.
    :type user: User
    :param all_tags: A comma-separated string of tag names.
    :type all_tags: str
    :param db: The database session.
    :type db: Session
    :return: The updated image, or None if it does not exist.
    :rtype: Image | None
    :raises HTTPException: If more than 5 tags are provided.
    """
    if user.role == Role.admin:
        exist_image = db.query(Image).filter(Image.id == image_id).first()
    else:
        exist_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    if exist_image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")
    try:
       if exist_image:
            tags = []
            list_tags = body.tags
            if len(list_tags) > 5:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can add up to 5 tags only.")
            for tag_name in list_tags:
                tag = db.query(Tag).filter(Tag.name == tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.add(tag)
                    db.commit()
                tags.append(tag)

            exist_image.qr_code = body.qr_code
            exist_image.description = body.description
            exist_image.edited_image = body.edited_image
            exist_image.tags = tags
            db.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Can't update image, {e}")
    return exist_image