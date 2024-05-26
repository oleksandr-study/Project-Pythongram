from typing import List

from fastapi import UploadFile, File, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from src.models.models import Image, User, Tag, Role
from src.schemas.images import ImageUpdateSchema

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


async def create_image(image_url, description, user: User, all_tags, db: Session) -> Image:
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

    print(f"now {image_url}")
    image = Image(
        image=image_url,
        #edited_image="image url",
        qr_code="none",
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
    if user.role ==Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()

    if image:
        db.delete(image)
        db.commit()
    return image


async def update_image(image_id: int, body: ImageUpdateSchema, user: User, all_tags, db: Session) -> Image | None:
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
    exist_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    if exist_image:
        tags = []
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

        exist_image.qr_code = body.qr_code
        exist_image.description = body.description
        exist_image.edited_image = body.edited_image
        exist_image.tags = tags
        db.commit()
    return exist_image