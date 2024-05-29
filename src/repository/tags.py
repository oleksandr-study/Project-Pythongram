from typing import List

from sqlalchemy.orm import Session
from src.models.models import Tag, User, Role


async def get_tags(skip: int, limit: int, db: Session, user: User
                   ) -> List[Tag] | None:
    """
    Retrieves a list of tags for a specific user.

    :param user: The user to retrieve tags for.
    :type user: User
    :param db: The database session.
    :type db: Session
    :return: A list of tags.
    :rtype: List[Tag]| None
    """
    tags =db.query(Tag).offset(skip).limit(limit).all()
    return tags


async def get_tag(tag_id: int, db: Session,user: User
                  ) -> Tag| None:
    """
    Retrieves a single tag by its ID.

    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param db: The database session.
    :type db: Session
    :return: The tag with the specified ID, or None if it does not exist.
    :rtype: Tag | None
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    return tag


async def remove_tag(tag_id: int, db: Session,user: User
                     ) -> Tag | None:
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
