from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


from src.models.models import User, Role


def get_role_by_name(name: str, db: AsyncSession) -> Role:
    """
    The get_role_by_name function takes a string and an AsyncSession object as arguments.
    It returns a Role object with the name of the string passed in.
    
    :param name: str: Specify the name of the role to be returned
    :param db: AsyncSession: Pass the database session to the function
    :return: A role object
    """
    role = Role[name]
    return role