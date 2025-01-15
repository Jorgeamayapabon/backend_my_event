from enum import Enum

class StatusEnum(str, Enum):
    """
    Enum representing the possible statuses of an event or process.

    Attributes:
        CREATED: Indicates that the event or process is newly created.
        ON_PROCESS: Indicates that the event or process is currently being processed.
        FINALIZED: Indicates that the event or process has been completed.
    """
    CREATED = "created"
    ON_PROCESS = "on-process"
    FINALIZED = "finalized"
    

class RoleEnum(str, Enum):
    """
    Enum representing the available roles for a user in the system.

    Attributes:
        OWNER: The user is the owner of the event or resource.
        ASSISTANT: The user assists with the event or resource.
    """
    OWNER = "owner"
    ASSISTANT = "assistant"


class RoleEnumInDB(str, Enum):
    """
    Enum representing the roles that a user can have in the database.

    Attributes:
        ADMIN: The user has administrative rights in the system.
        OWNER: The user is the owner of the event or resource.
        ASSISTANT: The user assists with the event or resource.
    """
    ADMIN = "admin"
    OWNER = "owner"
    ASSISTANT = "assistant"
