from enum import Enum


class StatusEnum(str, Enum):
    CREATED = "created"
    ON_PROCESS = "on-process"
    FINALIZED = "finalized"
    

class RoleEnum(str, Enum):
    OWNER = "owner"
    ASSISTANT = "assistant"
