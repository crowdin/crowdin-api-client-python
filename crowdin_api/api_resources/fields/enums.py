from enum import Enum


class FieldEntity(Enum):
    PROJECT = "project"
    USER = "user"
    TASK = "task"
    FILE = "file"
    TRANSLATION = "translation"
    STRING = "string"


class FieldType(Enum):
    CHECKBOX = "checkbox"
    RADIOBUTTONS = "radiobuttons"
    DATE = "date"
    DATETIME = "datetime"
    NUMBER = "number"
    LABELS = "labels"
    SELECT = "select"
    MULTISELECT = "multiselect"
    TEXT = "text"
    TEXTAREA = "textarea"
    URL = "url"


class FieldPlace(Enum):
    PROJECT_CREATE_MODAL = "projectCreateModal"
    PROJECT_HEADER = "projectHeader"
    PROJECT_DETAILS = "projectDetails"
    PROJECT_CROWDSOURCE_DETAILS = "projectCrowdsourceDetails"
    PROJECT_SETTINGS = "projectSettings"
    PROJECT_TASK_EDIT_CREATE = "projectTaskEditCreate"
    PROJECT_TASK_DETAILS = "projectTaskDetails"
    FILE_DETAILS = "fileDetails"
    FILE_SETTINGS = "fileSettings"
    USER_EDIT_MODAL = "userEditModal"
    USER_DETAILS = "userDetails"
    USER_POPOVER = "userPopover"
    STRING_EDIT_MODAL = "stringEditModal"
    STRING_DETAILS = "stringDetails"
    TRANSLATION_UNDER_CONTENT = "translationUnderContent"


class FieldOperations(Enum):
    REPLACE = "replace"


class FieldsPatchPath(Enum):
    NAME = "/name"
