from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from models.user import UserModel
from schemas.user import UserCreate, UserResponse, UserUpdate, UserUpdateAdmin

from services.user_services import UserServiceHandler
from utils.auths import get_current_user_with_role


router = APIRouter()


@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    service = UserServiceHandler(db)
    return service.list_users()


@router.post("", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    service = UserServiceHandler(db)
    return service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    service = UserServiceHandler(db)
    return service.get_user_by_id(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdateAdmin,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    service = UserServiceHandler(db)
    return service.update_user(user_id, user)


@router.patch("/me", response_model=UserResponse)
def update_user(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner", "assistant"])),
):
    service = UserServiceHandler(db)
    return service.update_user(current_user.id, user)


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin"])),
):
    service = UserServiceHandler(db)
    return service.delete_user(user_id)
