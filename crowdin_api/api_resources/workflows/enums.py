from enum import Enum


class ListWorkflowStepStringsOrderBy(Enum):
    ID = "id"
    TEXT = "text"
    IDENTIFIER = "identifier"
    CONTEXT = "context"
    CREATED_AT = "createdAt"
    UPDATED_AT = "updatedAt"
