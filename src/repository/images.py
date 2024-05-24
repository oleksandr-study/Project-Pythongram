from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from fastapi import APIRouter, HTTPException, Depends, status

from src.models.models import Image, User, Tag
from src.schemas.schemas import ImageModel, ImageUpdate


async def get_all_images(skip: int, limit: int, db: Session) -> List[Image]:
    return db.query(Image).offset(skip).limit(limit).all()

async def get_images_by_user(user_id: int, db: Session) -> List[Image]:
    user = db.query(User).filter(User.id == user_id).first()
    return db.query(Image).filter(Image.user_id == user.id).all()

  
async def get_images_by_id(image_id: int, db: Session) -> Image:

    image = db.query(Image).filter(Image.id == image_id).all()
    if image:
        image.comments = db.query(Comment).filter(Comment.image_id == image_id).all()
    return image



async def create_image(body: ImageModel, db: Session,#user: User
                       ) -> Image:
    if len(body.tags) > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can add up to 5 tags only.")
    tags = []
    for tag_name in body.tags:
        print(tag_name.name)
        tag = db.query(Tag).filter(Tag.name == tag_name.name).first()
        if not tag:
            tag = Tag(name=tag_name.name)
            db.add(tag)
            db.commit()
        tags.append(tag)
    # user = db.query(User).filter(User.id == 1).first()
    user_id = 3
    image = Image(
            image=body.image,
            edited_image="image url",
            qr_code=body.qr_code,
            user_id=11,
            description=body.description,
            tags=tags
        )

    db.add(image)
    db.commit()
    db.refresh(image)
    return image

async def remove_image(image_id: int, db: Session,  user: int) -> Image | None:
    image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user)).first()
    if image:
        db.delete(image)
        db.commit()
    return image


async def update_image(image_id: int, body: ImageUpdate, db: Session, user: int) -> Image | None:
    exist_image = db.query(Image).filter(and_(Image.id == image_id, Image.user_id == user)).first()
    if exist_image:
        if len(body.tags) > 5:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can add up to 5 tags only.")
        tags = []
        for tag_name in body.tags:
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