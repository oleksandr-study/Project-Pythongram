from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.schemas.comments import CommentBase, CommentResponse
from src.repository import comments
from src.services.auth import auth_service
from src.models.models import User,Role
from src.database.db import get_db
from typing import List

router = APIRouter(prefix='/images',tags=['comments'])

@router.get('/{image_id}/comments/',response_model=List[CommentResponse])
async def get_comments(image_id: int,db: Session = Depends(get_db)): #,current_user: User = Depends(auth_service.get_current_user)):
    all_comments = await comments.get_comments(db, image_id)#current_user.id)
    return all_comments

@router.post('/{image_id}/comments/', response_model=CommentResponse)
async def create_comment(image_id: int, body: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    return await comments.create_comment(image_id, body, db, current_user.id)

@router.patch('/comments/{comment_id}/', response_model=CommentResponse)
async def update_comm(comment_id: int, body: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await comments.update_comment(db,body,user_id=current_user.id, comment_id=comment_id)
    if comment is None:
         raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.delete('/comments/{comment_id}/', response_model=CommentResponse)
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    if current_user.role not in [Role.admin, Role.moderator]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    success = await comments.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return success