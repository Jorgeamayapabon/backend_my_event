from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.config import get_db
from models.user import UserModel
from schemas.category import CategoryCreate, CategoryResponse
from services.category_services import CategoryServiceHandler
from utils.auths import get_current_user_with_role

# Create an API router specifically for category-related endpoints
router = APIRouter()


@router.get("", response_model=List[CategoryResponse])
def list_categories(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Retrieve a list of all categories.

    Args:
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        List[CategoryResponse]: A list of category objects.
    """
    service = CategoryServiceHandler(db)
    return service.list_categories()


@router.post("", response_model=CategoryResponse)
def create_country(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user_with_role(["admin", "owner"])),
):
    """
    Create a new category.

    Args:
        category (CategoryCreate): The data required to create a category.
        db (Session): Database session dependency.
        current_user (UserModel): Current authenticated user with the roles "admin" or "owner".

    Returns:
        CategoryResponse: The newly created category object.
    """
    service = CategoryServiceHandler(db)
    return service.create_category(category)
