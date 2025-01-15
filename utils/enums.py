from enum import Enum


class StatusEnum(str, Enum):
    CREATED = "created"
    ON_PROCESS = "on-process"
    FINALIZED = "finalized"
    

class RoleEnum(str, Enum):
    OWNER = "owner"
    ASSISTANT = "assistant"


class RoleEnumInDB(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    ASSISTANT = "assistant"
