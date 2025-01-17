from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from db.config import get_db
from models.user import UserModel
from utils.constants import ALGORITHM, SECRET_KEY
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# OAuth2 password bearer for token management
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Predefined exceptions for different error scenarios
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
USER_INACTIVE_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Inactive user",
)
NO_HAS_PERMISSION_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No has permission",
    headers={"WWW-Authenticate": "Bearer"}
)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Retrieves the current user based on the provided JWT token.

    Args:
        db (Session): The database session to query the user model.
        token (str): The JWT token passed from the client.

    Returns:
        UserModel: The user model of the authenticated user.

    Raises:
        HTTPException: If the token is invalid or if the user is not found.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise CREDENTIALS_EXCEPTION

    return user


def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    """
    Retrieves the current active user. If the user is inactive, raises an exception.

    Args:
        current_user (UserModel): The authenticated user.

    Returns:
        UserModel: The authenticated active user.

    Raises:
        HTTPException: If the user is inactive.
    """
    if not current_user.active:
        raise USER_INACTIVE_EXCEPTION
    return current_user


def has_role(current_user: UserModel, roles: List[str]):
    """
    Checks if the current user has one of the specified roles.

    Args:
        current_user (UserModel): The user to check roles.
        roles (List[str]): A list of roles to check.

    Returns:
        bool: True if the user has any of the roles, False otherwise.
    """
    return current_user.role in roles


def get_current_user_with_role(roles: List[str]):
    """
    Dependency to retrieve the current user with a specified role.

    Args:
        roles (List[str]): A list of roles to check against the current user's role.

    Returns:
        function: A FastAPI dependency function that checks if the user has the required role.

    Raises:
        HTTPException: If the user does not have the required role.
    """
    def dependency(current_user: UserModel = Depends(get_current_active_user)):
        if not has_role(current_user, roles):
            raise NO_HAS_PERMISSION_EXCEPTION
        return current_user
    return dependency
