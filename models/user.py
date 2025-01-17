from sqlalchemy import Boolean, Column, Integer, String, Enum as SQLAlchemyEnum
from db.config import Base
from sqlalchemy.orm import relationship

from models.base import DatetimeModel
from utils.enums import RoleEnumInDB


class UserModel(Base, DatetimeModel):
    """
    Represents a user in the system.

    This model extends the `DatetimeModel` to include timestamps (`created_at` and `updated_at`). 
    It contains attributes for managing user data, such as the full name, email, role, and password hash.
    Additionally, it defines a relationship with the `EventModel` to associate users with events they own.

    Attributes:
        id (Column): The unique identifier for the user.
        fullname (Column): The full name of the user.
        email (Column): The email address of the user, must be unique.
        active (Column): A boolean indicating whether the user's account is active (default: True).
        role (Column): The role of the user, represented as an enum (`RoleEnumInDB`).
        hashed_password (Column): The hashed password of the user.
        events (relationship): A relationship to the `EventModel` for events owned by the user.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, doc="The unique identifier for the user.")
    fullname = Column(String, nullable=False, doc="The full name of the user.")
    email = Column(String, nullable=False, unique=True, doc="The unique email address of the user.")
    active = Column(Boolean, default=True, doc="Indicates whether the user's account is active. Default is True.")
    role = Column(SQLAlchemyEnum(RoleEnumInDB), nullable=False, doc="The role of the user (enum from RoleEnumInDB).")
    hashed_password = Column(String, nullable=False, doc="The hashed password for user authentication.")

    # Relationship to the EventModel for events owned by this user
    events = relationship("EventModel", back_populates="owner", doc="Relationship to the EventModel for events owned by the user.")
