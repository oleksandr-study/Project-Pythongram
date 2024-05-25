from sqlalchemy.orm import Session
from src.models.models import User,Comment
from src.schemas.comments import CommentBase
from typing import List
from sqlalchemy import and_

async def get_comments(db: Session, image_id: int) -> List[Comment]:
    return db.query(Comment).filter(Comment.image_id == image_id).all()

async def get_comment(db: Session, image_id: int ) -> Comment:
    return db.query(Comment).filter(Comment.image_id == image_id).first()

async def create_comment(image_id: int, comment:CommentBase, db: Session, user_id: int) -> Comment:
    db_comment = Comment(comment=comment.comment, 
                         user_id=user_id, 
                         image_id=image_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

async def update_comment(db: Session, body: CommentBase,user_id:int ,comment_id: int) -> Comment | None:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id, Comment.user_id == user_id)).first()
    if comment: 
        comment.comment = body.comment
        db.commit()

    return comment

async def delete_comment(db: Session, comment_id: int) -> Comment | None:
    comment = db.query(Comment).filter(and_(Comment.id == comment_id)).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment