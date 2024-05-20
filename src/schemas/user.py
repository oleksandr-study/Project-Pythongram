from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.models.models import Role
from typing import Optional

class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=8)


class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: EmailStr
    avatar: str | None
    role: Role
    created_at: datetime
    photos_uploaded: int| None
    model_config = ConfigDict(from_attributes = True)  # noqa

            
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr