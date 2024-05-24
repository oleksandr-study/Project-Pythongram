from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas.tags import TagModel, TagResponse
from src.repository import tags as repository_tags

router = APIRouter(prefix='/tags', tags=["tags"])


@router.get("/", response_model=List[TagResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of tags with pagination.

    :param skip: The number of tags to skip.
    :type skip: int
    :param limit: The maximum number of tags to return.
    :type limit: int
    :param db: The database session.
    :type db: Session
    :return: A list of tags.
    :rtype: List[TagResponse]
    """
    tags = await repository_tags.get_tags(skip, limit, db)
    return tags


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a tag by its ID.

    :param tag_id: The ID of the tag to retrieve.
    :type tag_id: int
    :param db: The database session.
    :type db: Session
    :return: The tag with the specified ID, or raises a 404 error if not found.
    :rtype: TagResponse
    """
    tag = await repository_tags.get_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.delete("/{tag_id}", response_model=TagResponse)
async def remove_tag(tag_id: int, db: Session = Depends(get_db)):
    """
    Deletes a tag by its ID.

    :param tag_id: The ID of the tag to delete.
    :type tag_id: int
    :param db: The database session.
    :type db: Session
    :return: The deleted tag, or raises a 404 error if not found.
    :rtype: TagResponse
    """
    tag = await repository_tags.remove_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag