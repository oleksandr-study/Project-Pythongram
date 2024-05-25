from typing import List

from fastapi import UploadFile, File, HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status

from src.models.models import Image, User, Tag, Role
from src.schemas.images import ImageUpdateSchema

async def get_all_images(skip: int, limit: int, db: Session) -> List[Image]:
    return db.query(Image).offset(skip).limit(limit).all()


async def get_images_by_user(user_id: int, db: Session) -> List[Image]:
    user = db.query(User).filter(User.id == user_id).first()
    return db.query(Image).filter(Image.user_id == user.id).all()


async def get_images_by_id(image_id: int, user: User, db: Session) -> Image:
    return db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).all()


async def create_image(image_url, description, user: User, all_tags, db: Session) -> Image:
    tags = []
    list_tags = all_tags.split(", ")
    print(all_tags)
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
    if user.role ==Role.admin:
        image = db.query(Image).filter(Image.id == image_id).first()
    else:
        image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()

    if image:
        db.delete(image)
        db.commit()
    return image


async def update_image(image_id: int, body: ImageUpdateSchema, user: User, db: Session) -> Image | None:
    exist_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user.id)).first()
    if exist_image:
        tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        exist_image.qr_code = body.qr_code
        exist_image.description = body.description
        exist_image.edited_image = body.edited_image
        exist_image.tags = tags
        db.commit()
    return exist_image