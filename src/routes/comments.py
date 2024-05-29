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
async def get_comments(image_id: int, db: Session = Depends(get_db)): #,current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_comments function returns all comments for a given image_id.
        
    
    :param image_id: int: Get the comments for a specific image
    :param db: Session: Pass the database session to the function
    :return: A list of comments
    """
    all_comments = await comments.get_comments(image_id, db)#current_user.id)
    return all_comments

@router.post('/{image_id}/comments/', response_model=CommentResponse)
async def create_comment(image_id: int, body: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_comment function creates a new comment for the image with the given id.
        The body of the request should be in JSON format and contain:
            - body (string): The text content of the comment.
    
    :param image_id: int: Specify the image that the comment is being made on
    :param body: CommentBase: Pass the comment body to the function
    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the user that is currently logged in
    :return: A comment object
    """
    return await comments.create_comment(image_id, body, db, current_user.id)

@router.patch('/comments/{comment_id}/', response_model=CommentResponse)
async def update_comm(comment_id: int, body: CommentBase, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The update_comm function updates a comment in the database.
        Args:
            comment_id (int): The id of the comment to update.
            body (CommentBase): The updated information for the Comment object.
        Returns:
            A Comment object with updated information.
    
    :param comment_id: int: Identify the comment that is being updated
    :param body: CommentBase: Pass the comment object to the update_comment function
    :param db: Session: Pass in the database session from the dependency injection
    :param current_user: User: Get the current user from the auth_service
    :return: A comment object
    """
    comment = await comments.update_comment(comment_id, body, db, current_user.id)
    if comment is None:
         raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.delete('/comments/{comment_id}/', response_model=CommentResponse)
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The delete_comment function deletes a comment from the database.
        The function takes in an integer representing the id of the comment to be deleted, and returns a boolean value indicating whether or not it was successful.
    
    :param comment_id: int: Specify the comment id of the comment to be deleted
    :param db: Session: Pass the database connection to the function
    :param current_user: User: Get the current user from the database
    :return: A boolean, which is a bit of an odd choice
    """
    if current_user.role not in [Role.admin, Role.moderator]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    success = await comments.delete_comment(comment_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return success