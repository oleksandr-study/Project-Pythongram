
"""
User repository module.

This module contains the functions to interact with the UserDB model in the database.
It includes functions to get a user by email, create a new user, update a user's token,
confirm a user's email, and update a user's avatar.
"""

from src.models.models import User
from sqlalchemy.orm import Session
from src.schemas.user import UserModel
from libgravatar import Gravatar 



async def get_user_by_email(email: str, db: Session) -> User:
    """
    Retrieves a user from the database by their email.

    :param email: The email of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email, or None if the user does not exist.
    :rtype: UserDB | None
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    Creates a new user in the database.

    :param body: The data for the new user.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: UserDB
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    users = db.query(User).all()
    if not users:
        new_user.role = "admin"
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Updates the refresh token for a user.

    :param user: The user to update the token for.
    :type user: UserDB
    :param token: The new refresh token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    Marks a user's email as confirmed.

    :param email: The email of the user to confirm.
    :type email: str
    :param db: The database session.
    :type db: Session
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

# async def update_avatar(email: str, avatar_path: str, db: Session) -> UserDB:
#     print(email)
#     user = db.query(UserDB).filter(UserDB.email == email).first()
#     print(user)
#     user.avatar = avatar_path
#     db.commit()
#     db.refresh(user)
#     return user

async def update_avatar(email, url: str, db: Session) -> User:
    """
    Updates the avatar for a user with the given email.
    Using the service Cloudinary
    This function retrieves the user by their email, updates their avatar URL,
    commits the changes to the database, and refreshes the user object to include
    the updated avatar URL.

    :param email: The email of the user whose avatar is to be updated.
    :type email: str
    :param url: The new URL of the avatar image.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The updated user object.
    :rtype: UserDB
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def update_user_role(email: str, new_role: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user