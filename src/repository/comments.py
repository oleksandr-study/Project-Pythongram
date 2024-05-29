from sqlalchemy.orm import Session
from src.models.models import User,Comment
from src.schemas.comments import CommentBase
from typing import List
from sqlalchemy import and_

async def get_comments(image_id: int,db: Session) -> List[Comment]:
    """
    Retrieves a list of comments for a specific image.

    :param image_id: The ID of the image to retrieve comments for.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :return: A list of comments for the specified image.
    :rtype: List[Comment]
    """
    return db.query(Comment).filter(Comment.image_id == image_id).all()

async def get_comment(image_id: int, db: Session) -> Comment:
    """
    Retrieves a single comment for a specific image.

    :param image_id: The ID of the image to retrieve a comment for.
    :type image_id: int
    :param db: The database session.
    :type db: Session
    :return: The first comment for the specified image, or None if it does not exist.
    :rtype: Comment | None
    """
    return db.query(Comment).filter(Comment.image_id == image_id).first()

async def create_comment(image_id: int, comment:CommentBase, db: Session, user_id: int) -> Comment:
    """
    Creates a new comment for a specific image.

    :param image_id: The ID of the image to create the comment for.
    :type image_id: int
    :param comment: The data for the comment to create.
    :type comment: CommentBase
    :param db: The database session.
    :type db: Session
    :param user_id: The ID of the user creating the comment.
    :type user_id: int
    :return: The newly created comment.
    :rtype: Comment
    """
    db_comment = Comment(comment=comment.comment, 
                         user_id=user_id, 
                         image_id=image_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

async def update_comment(comment_id: int, body: CommentBase, db: Session, user_id:int) -> Comment | None:
    """
    Updates a comment with the specified ID for a specific user.

    :param comment_id: The ID of the comment to update.
    :type comment_id: int
    :param body: The updated data for the comment.
    :type body: CommentBase
    :param db: The database session.
    :type db: Session
    :param user_id: The ID of the user updating the comment.
    :type user_id: int
    :return: The updated comment, or None if it does not exist.
    :rtype: Comment | None
    """
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user_id)).first()
    if comment: 
        comment.comment = body.comment
        db.commit()

    return comment

async def delete_comment(comment_id: int, db: Session) -> Comment | None:
    """
    Deletes a comment with the specified ID.

    :param comment_id: The ID of the comment to delete.
    :type comment_id: int
    :param db: The database session.
    :type db: Session
    :return: The deleted comment, or None if it does not exist.
    :rtype: Comment | None
    """
    comment = db.query(Comment).filter(and_(Comment.id == comment_id)).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment