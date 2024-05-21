from fastapi import APIRouter, HTTPException, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.database.db import get_db
from src.repository import users as repository_users
# from src.repository import photos as repository_photos
from src.services.auth import auth_service
from src.models.models import User
from src.schemas.user import UserResponse
router = APIRouter(prefix='/user_option', tags=['user_option'])
security = HTTPBearer()


@router.get("/username", response_model=UserResponse)
async def get_user_profile(username: str, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    user = repository_users.get_user_by_username(username, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    photos_uploaded = await repository_users.count_user_photos(username, db)  # Підрахунок кількості фотографій користувача
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        avatar=user.avatar,
        role=user.role,
        created_at=user.created_at,
        photos_uploaded=photos_uploaded  # Додаємо кількість фотографій користувача до відповіді
    )                