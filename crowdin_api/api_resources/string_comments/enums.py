from enum import Enum


class StringCommentType(Enum):
    COMMENT = "comment"
    ISSUE = "issue"


class StringCommentIssueType(Enum):
    GENERAL_QUESTION = "general_question"
    TRANSLATION_MISTAKE = "translation_mistake"
    CONTEXT_REQUEST = "context_request"
    SOURCE_MISTAKE = "source_mistake"


class StringCommentIssueStatus(Enum):
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"


class StringCommentPatchPath(Enum):
    TEXT = "/text"
    ISSUE_STATUS = "/issueStatus"


class ListStringCommentsOrderBy(Enum):
    ID = "id"
    TEXT = "text"
    TYPE = "type"
    CREATED_AT = "createdAt"
    RESOLVED_AT = "resolvedAt"
    ISSUE_STATUS = "issueStatus"
    ISSUE_TYPE = "issueType"
