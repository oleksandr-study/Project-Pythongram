from typing import Optional

from fastapi import Request, Depends, HTTPException, status

import sys
from pathlib import Path


# Добавляем корневую папку проекта в sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.models.models import Role, User
from src.services.auth import Auth


class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: list[Role]: Define the allowed roles for a user
        :return: The object itself
        """
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(Auth.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
        It takes in two arguments: request and user. The request argument is the Request object, which contains all of 
        the information about the HTTP request (headers, body, etc.). The user argument is a User object that we get from 
        calling Auth.get_current_user(). This function returns nothing.
        
        :param self: Refer to the current instance of a class
        :param request: Request: Access the request object
        :param user: User: Get the user object from the request
        :return: The user object
        """
        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN"
            )