#services.auth.py
from typing import Optional, List

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

import sys
from pathlib import Path

# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.models.models import User, Role

from src.database.db import get_db
from src.repository import users as repository_users
from src.repository import roles as repository_roles
from src.conf.config import settings


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm 

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, Auth.SECRET_KEY, algorithm=Auth.ALGORITHM)
        return encoded_access_token

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, Auth.SECRET_KEY, algorithm=Auth.ALGORITHM)
        return encoded_refresh_token

    @staticmethod
    def decode_refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, Auth.SECRET_KEY, algorithms=[Auth.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db),
                               role: Role = None):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, Auth.SECRET_KEY, algorithms=[Auth.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception

        if role and user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")

        return user
    
    @staticmethod
    def change_user_role(admin_email: str, user_email: str, new_role: str, db: Session = Depends(get_db)):
        admin = repository_users.get_user_by_email(admin_email, db)
        if admin is None or admin.role != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can change user roles")

        user = repository_users.get_user_by_email(user_email, db)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.role = new_role
        repository_users.update_user_role(user.email, user.role, db)

        return {"message": "Role updated successfully"}
    
    def create_email_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def get_email_from_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")

auth_service = Auth()
