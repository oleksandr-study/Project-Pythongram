from typing import List

from sqlalchemy.orm import Session

from src.models.models import Tag
from src.schemas.tags import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    """
    Retrieves a list of tags for a specific user.

    :param user: The user to retrieve tags for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of tags.
    :rtype: List[Tag]
    """
    return db.query(Tag).offset(skip).limit(limit).all()


async def get_tag(tag_id: int, db: Session) -> Tag:
    """
    Retrieves a single tag by its ID.

    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param db: The database session.
    :type db: Session
    :return: The tag with the specified ID, or None if it does not exist.
    :rtype: Tag | None
    """
    return db.query(Tag).filter(Tag.id == tag_id).first()


async def create_tag(body: TagModel, db: Session) -> Tag:
    """
    Creates a new tag for a specific user.

    :param body: The data for the tag to create.
    :type body: TagModel
    :param user: The user to create the tag for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The newly created tag.
    :rtype: Tag
    """
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    """
    Updates a tag with the specified ID for a specific user.

    :param tag_id: The ID of the tag to update.
    :type tag_id: int
    :param body: The updated data for the tag.
    :type body: TagModel
    :param user: The user to update the tag for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The updated tag, or None if it does not exist.
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        tag.name = body.name
        db.commit()
    return tag


async def remove_tag(tag_id: int, db: Session) -> Tag | None:
    """
    Deletes a tag with the specified ID for a specific user.

    :param tag_id: The ID of the tag to delete.
    :type tag_id: int
    :param user: The user to delete the tag for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: The deleted tag, or None if it does not exist.
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
