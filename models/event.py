from db.config import Base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Text,
    Enum as SQLAlchemyEnum,
)
from sqlalchemy.orm import relationship

from models.base import DatetimeModel
from utils.enums import StatusEnum


class EventModel(Base, DatetimeModel):
    """
    Represents an event in the system.

    This model extends the `DatetimeModel` to include timestamps (`created_at` and `updated_at`)
    and provides attributes for managing event data, such as name, description, date, and status.
    It also defines relationships to other models, such as `CityModel`, `CategoryModel`, and `UserModel`.

    Attributes:
        id (Column): The unique identifier for the event.
        name (Column): The name of the event.
        description (Column): A detailed description of the event.
        date (Column): The date and time when the event occurs.
        capacity (Column): The maximum number of attendees allowed.
        status (Column): The current status of the event, defined by `StatusEnum`.
        location_id (Column): The ID of the associated city where the event takes place.
        category_id (Column): The ID of the category to which the event belongs.
        owner_id (Column): The ID of the user who owns or organizes the event.
        location (relationship): A relationship to the `CityModel` for the event's location.
        category (relationship): A relationship to the `CategoryModel` for event categorization.
        tickets (relationship): A relationship to the `EventTicketModel` for tracking event tickets.
        sessions (relationship): A relationship to the `SessionModel` for event sessions.
        owner (relationship): A relationship to the `UserModel` for the event organizer/owner.
    """

    __tablename__ = "event"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="The unique identifier for the event.",
    )
    name = Column(String, nullable=False, doc="The name of the event.")
    description = Column(
        Text, nullable=True, doc="A detailed description of the event."
    )
    date = Column(
        DateTime, nullable=False, doc="The date and time when the event occurs."
    )
    capacity = Column(
        Integer, nullable=False, doc="The maximum number of attendees allowed."
    )
    status = Column(
        SQLAlchemyEnum(StatusEnum),
        nullable=False,
        doc="The current status of the event.",
    )
    location_id = Column(
        Integer,
        ForeignKey("city.id"),
        nullable=False,
        doc="The ID of the associated city for event location.",
    )
    category_id = Column(
        Integer,
        ForeignKey("category.id"),
        nullable=False,
        doc="The ID of the category to which the event belongs.",
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="The ID of the user who owns the event.",
    )

    # Relationships to other models
    location = relationship(
        "CityModel",
        back_populates="events",
        doc="Relationship to the CityModel representing the event's location.",
    )
    category = relationship(
        "CategoryModel",
        # back_populates="events",
        doc="Relationship to the CategoryModel for event categorization.",
    )
    tickets = relationship(
        "EventTicketModel",
        back_populates="event",
        doc="Relationship to the EventTicketModel to track event tickets.",
    )
    sessions = relationship(
        "SessionModel",
        back_populates="event",
        doc="Relationship to the SessionModel for event sessions.",
    )
    owner = relationship(
        "UserModel",
        back_populates="events",
        doc="Relationship to the UserModel representing the event owner.",
    )


class SessionModel(Base, DatetimeModel):
    """
    Represents a session within an event.

    This model extends the `DatetimeModel` to include timestamps and defines attributes
    for managing session details, such as name, description, timing, and speaker.

    Attributes:
        id (Column): The unique identifier for the session.
        event_id (Column): The ID of the associated event to which this session belongs.
        name (Column): The name of the session.
        description (Column): A detailed description of the session.
        start_time (Column): The start time of the session.
        end_time (Column): The end time of the session.
        capacity (Column): The maximum number of attendees allowed for the session.
        speaker (Column): The name of the speaker for the session.
        event (relationship): A relationship to the `EventModel` for the associated event.
    """

    __tablename__ = "session"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="The unique identifier for the session.",
    )
    event_id = Column(
        Integer,
        ForeignKey("event.id"),
        nullable=False,
        doc="The ID of the associated event.",
    )
    name = Column(String, doc="The name of the session.")
    description = Column(Text, doc="A detailed description of the session.")
    start_time = Column(DateTime, doc="The start time of the session.")
    end_time = Column(DateTime, doc="The end time of the session.")
    capacity = Column(
        Integer, doc="The maximum number of attendees allowed for the session."
    )
    speaker = Column(String, doc="The name of the speaker for the session.")

    event = relationship(
        "EventModel",
        back_populates="sessions",
        doc="Relationship to the EventModel for the associated event.",
    )


class EventTicketModel(Base, DatetimeModel):
    """
    Represents a ticket for an event.

    This model extends the `DatetimeModel` and defines attributes for tracking tickets
    issued for an event, associating a user with a specific event.

    Attributes:
        id (Column): The unique identifier for the event ticket.
        event_id (Column): The ID of the event for which the ticket is issued.
        user_id (Column): The ID of the user who owns the ticket.
        event (relationship): A relationship to the `EventModel` for the associated event.
        user (relationship): A relationship to the `UserModel` for the user who owns the ticket.
    """

    __tablename__ = "event_ticket"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="The unique identifier for the event ticket.",
    )
    event_id = Column(
        Integer,
        ForeignKey("event.id"),
        nullable=False,
        doc="The ID of the event for which the ticket is issued.",
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="The ID of the user who owns the ticket.",
    )

    # Relationships to other models
    event = relationship(
        "EventModel",
        back_populates="tickets",
        doc="Relationship to the EventModel for the associated event.",
    )
    user = relationship(
        "UserModel",
        doc="Relationship to the UserModel for the user who owns the ticket.",
    )
