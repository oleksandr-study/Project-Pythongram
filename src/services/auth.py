# src.auth.auth.py

"""
Authentication module.

This module contains the Auth class, which is responsible for handling
authentication-related operations such as password hashing, token creation,
token decoding, and user retrieval from the database.
"""

import redis
import pickle
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from starlette import status
from  src.database.db import get_db
from src.repository import users as repository_users
from src.conf.config import settings
from src.models.models import Role


class Auth:
    """
    Authentication service class.

    This class provides methods for password hashing, token creation,
    token decoding, and user retrieval from the database.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = settings.secret_key
    ALGORITHM = settings.algorithm
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)

    def verify_password(self, plain_password, hashed_password):
        """
        Verify a plain password against a hashed password.

        :param plain_password: The plain password to verify.
        :type plain_password: str
        :param hashed_password: The hashed password to compare against.
        :type hashed_password: str
        :return: True if the passwords match, False otherwise.
        :rtype: bool
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Hash a password.

        :param password: The password to hash.
        :type password: str
        :return: The hashed password.
        :rtype: str
        """
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create a new access token.

        :param data: The data to encode in the token.
        :type data: dict
        :param expires_delta: The number of seconds the token should expire after.
        :type expires_delta: Optional[float]
        :return: The encoded access token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    # define a function to generate a new refresh token
    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create a new refresh token.

        :param data: The data to encode in the token.
        :type data: dict
        :param expires_delta: The number of seconds the token should expire after.
        :type expires_delta: Optional[float]
        :return: The encoded refresh token.
        :rtype: str
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        Decode a refresh token.

        :param refresh_token: The refresh token to decode.
        :type refresh_token: str
        :return: The email contained in the refresh token.
        :rtype: str
        :raises HTTPException: If the token is invalid or has an invalid scope.
        """
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Retrieve the current user from the database using a JWT token.

        :param token: The JWT token.
        :type token: str
        :param db: The database session.
        :type db: Session
        :return: The current user.
        :rtype: UserDB
        :raises HTTPException: If the token is invalid or has an invalid scope.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception
        user = self.r.get(f"user:{email}")
        if user is None:
            user = await repository_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            self.r.set(f"user:{email}", pickle.dumps(user))
            self.r.expire(f"user:{email}", 900)
        else:
            user = pickle.loads(user)
        return user
    
    def create_email_token(self, data: dict):
        """
        Create a new email token.

        :param data: The data to encode in the token.
        :type data: dict
        :return: The encoded email token.
        :rtype: str
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=1)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token
    
    async def get_email_from_token(self, token: str):
        """
        Retrieve the email from a JWT token.

        :param token: The JWT token.
        :type token: str
        :return: The email contained in the token.
        :rtype: str
        :raises HTTPException: If the token is invalid.
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")




    async def change_user_role(self, admin_email: str, user_email: str, new_role: str, db: Session = Depends(get_db)):
        admin = await repository_users.get_user_by_email(admin_email, db)
        if admin is None or admin.role != Role.admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can change user roles")

        user = await repository_users.get_user_by_email(user_email, db)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.role = new_role
        await repository_users.update_user_role(user.email, user.role, db)

        return {"message": "Role updated successfully"}
    
auth_service = Auth()