from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import EmailStr

class UserModel(BaseModel):
    """
    Pydantic model for a User.

    This model defines the fields for a user.

    - username: The username of the user.
    - email: The email of the user.
    - password: The password of the user.
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Pydantic model for a User in the database.

    This model defines the fields for a user in the database.

    - id: The id of the user.
    - username: The username of the user.
    - email: The email of the user.
    - created_at: The date and time the user was created.
    - avatar: The URL of the user's avatar.
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Pydantic model for a User response.

    This model defines the response schema for a user.

    - user: The user object.
    - detail: A message indicating that the user was successfully created.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Pydantic model for a Token.

    This model defines the fields for a token.

    - access_token: The access token.
    - refresh_token: The refresh token.
    - token_type: The type of the token.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
    
class RequestEmail(BaseModel):
    """
    Pydantic model for an Email request.

    This model defines the fields for an email request.

    - email: The email address.
    """ 
    email: EmailStr
