from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from models.user import UserModel
from schemas.user import UserCreate, UserResponse, UserUpdate, UserUpdateAdmin
from services.user_services import UserServiceHandler
from utils.auths import get_current_user_with_role

# Create a router for user-related endpoints
router = APIRouter()


@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    """
    Retrieve a list of all users.

    Args:
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the role "admin".

    Returns:
        List[UserResponse]: A list of user objects.
    """
    service = UserServiceHandler(db)
    return service.list_users()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user (UserCreate): The data required to create a user.
        db (Session): Database session dependency.

    Returns:
        UserResponse: The newly created user object.
    """
    service = UserServiceHandler(db)
    return service.create_user(user, db)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    """
    Retrieve details of a specific user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the role "admin".

    Returns:
        UserResponse: The user object with the specified ID.
    """
    service = UserServiceHandler(db)
    return service.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdateAdmin,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    """
    Update details of a specific user by an admin.

    Args:
        user_id (int): The ID of the user to update.
        user (UserUpdateAdmin): The data to update for the user.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the role "admin".

    Returns:
        UserResponse: The updated user object.
    """
    service = UserServiceHandler(db)
    return service.update_user(user_id, user)


@router.patch("/me", response_model=UserResponse)
def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner", "assistant"])),
):
    """
    Update details of the currently authenticated user.

    Args:
        user (UserUpdate): The data to update for the current user.
        db (Session): Database session dependency.
        current_user (UserModel): The currently authenticated user.

    Returns:
        UserResponse: The updated user object.
    """
    service = UserServiceHandler(db)
    return service.update_user(current_user.id, user)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the role "admin".

    Returns:
        UserResponse: The deleted user object.
    """
    service = UserServiceHandler(db)
    return service.delete_user(user_id)
