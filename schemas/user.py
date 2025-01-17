from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

from schemas import DatetimeSchema
from utils.enums import RoleEnum


class UserBase(BaseModel):
    """
    A base schema for user-related operations.

    This schema defines the core attributes for a user model, used for creating 
    or updating user records. It contains essential fields like fullname, email, 
    account status, and user role.

    Attributes:
        fullname (str): The full name of the user.
        email (EmailStr): The email address of the user.
        active (bool): A boolean indicating whether the user is active.
        role (RoleEnum): The role assigned to the user (e.g., admin, user).
    """
    fullname: str
    email: EmailStr
    active: bool
    role: RoleEnum


class UserUpdateAdmin(BaseModel):
    """
    A schema for updating user details as an admin.

    This schema allows admins to update any of the user attributes including 
    fullname, email, account status, and role. All fields are optional, so any 
    field can be updated independently.

    Attributes:
        fullname (Optional[str]): The full name of the user (optional).
        email (Optional[EmailStr]): The email address of the user (optional).
        active (Optional[bool]): A boolean indicating whether the user is active (optional).
        role (Optional[RoleEnum]): The role assigned to the user (optional).
    """
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None
    role: Optional[RoleEnum] = None


class UserUpdate(BaseModel):
    """
    A schema for updating user details by the user themselves.

    This schema allows users to update their own details, such as fullname, 
    email, and account status. Role is excluded, as users should not be able 
    to modify their role.

    Attributes:
        fullname (Optional[str]): The full name of the user (optional).
        email (Optional[EmailStr]): The email address of the user (optional).
        active (Optional[bool]): A boolean indicating whether the user is active (optional).
    """
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    active: Optional[bool] = None


class UserInDB(UserBase):
    """
    A schema for representing a user stored in the database.

    This schema includes the user details as stored in the database, which 
    includes the hashed password for authentication. It inherits from `UserBase` 
    and adds the `hashed_password` field.

    Attributes:
        fullname (str): The full name of the user (inherited from UserBase).
        email (EmailStr): The email address of the user (inherited from UserBase).
        active (bool): A boolean indicating whether the user is active (inherited from UserBase).
        role (RoleEnum): The role assigned to the user (inherited from UserBase).
        hashed_password (str): The hashed password of the user for authentication.
    """
    hashed_password: str


class UserCreate(UserBase):
    """
    A schema for creating a new user.

    This schema is used for creating a new user and includes the password 
    field, which will be hashed before storing it in the database.

    Attributes:
        fullname (str): The full name of the user (inherited from UserBase).
        email (EmailStr): The email address of the user (inherited from UserBase).
        active (bool): A boolean indicating whether the user is active (inherited from UserBase).
        role (RoleEnum): The role assigned to the user (inherited from UserBase).
        password (str): The password of the user to be hashed before storage.
    """
    password: str


class UserResponse(UserBase, DatetimeSchema):
    """
    A schema for representing a user in response data.

    This schema includes user information along with timestamps for creation 
    and updates. It is used for sending back user details in API responses.

    Attributes:
        id (int): The unique identifier for the user.
        fullname (str): The full name of the user (inherited from UserBase).
        email (EmailStr): The email address of the user (inherited from UserBase).
        active (bool): A boolean indicating whether the user is active (inherited from UserBase).
        role (RoleEnum): The role assigned to the user (inherited from UserBase).
        created_at (datetime): The timestamp when the user was created (inherited from DatetimeSchema).
        updated_at (datetime): The timestamp when the user was last updated (inherited from DatetimeSchema).
    """
    id: int
    
    class Config:
        """
        Configurations for the schema, allowing ORM models to be used directly.

        The `orm_mode = True` setting allows Pydantic to read data from ORM models and 
        convert them into Pydantic models.
        """
        orm_mode = True
