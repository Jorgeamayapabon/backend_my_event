from pydantic import BaseModel
from schemas import DatetimeSchema


class CategoryBase(BaseModel):
    """
    A base schema for category-related operations.

    This schema defines the common attributes shared by category models such as 
    the category's name. It is inherited by other schemas that define more specific 
    attributes for creating or responding to category data.

    Attributes:
        name (str): The name of the category.
    """
    name: str


class CategoryCreate(CategoryBase):
    """
    A schema for creating a new category.

    Inherits from `CategoryBase` and does not add any new attributes.
    It is used for request bodies when creating a category.

    Attributes:
        name (str): The name of the category (inherited from CategoryBase).
    """
    pass


class CategoryResponse(CategoryBase, DatetimeSchema):
    """
    A schema for representing a category in response data.

    Inherits from both `CategoryBase` and `DatetimeSchema` to include category 
    information along with the timestamps for creation and updates.

    Attributes:
        id (int): The unique identifier for the category.
        name (str): The name of the category (inherited from CategoryBase).
        created_at (datetime): The timestamp when the category was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the category was last updated (inherited from DatetimeSchema).
    """
    id: int

    class Config:
        """
        Configurations for the schema, such as allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True
