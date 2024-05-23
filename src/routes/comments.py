from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.schemas import CommentBase,CommentResponse
from repository import comments
from services.auth import auth_service
from models.models import User,Role
from database.db import get_db
from typing import List

router = APIRouter(prefix='/images',tags=['images'])

@router.get('/{image_id}/comments/',response_model=List[CommentResponse])
async def get_comments(db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user)):
    all_comments = await comments.get_comments(db,current_user.id)
    return all_comments

@router.post('/{image_id}/comments/', response_model=CommentResponse)
async def create_comment(image_id: int, body: CommentBase, db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user)):
    return await comments.create_comment(image_id,body,db,current_user.id)

@router.patch('/{image_id}/comments/{comment_id}/', response_model=CommentResponse)
async def update_comm(comment_id: int, body: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    comment = await comments.get_comment(comment_id,body,db,current_user.id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.delete('/{image_id}/comments/{comment_id}/', response_model=CommentResponse, status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    if current_user.role not in [Role.admin, Role.moderator]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    success = await comments.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return success
