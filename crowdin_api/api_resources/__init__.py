from .advisors.resource import AdvisorsResource
from .ai.resource import AIResource, EnterpriseAIResource
from .application.resource import ApplicationResource
from .branches.resource import BranchesResource
from .bundles.resource import BundlesResource
from .clients.resource import ClientsResource
from .custom_placeholders.resource import CustomPlaceholdersResource
from .custom_spellcheckers.resource import CustomSpellcheckersResource
from .dictionaries.resource import DictionariesResource
from .distributions.resource import DistributionsResource
from .external_qa_checks.resource import ExternalQaChecksResource
from .fields.resource import FieldsResource
from .glossaries.resource import GlossariesResource
from .groups.resource import GroupsResource
from .labels.resource import LabelsResource
from .languages.resource import LanguagesResource
from .machine_translation_engines.resource import (
    EnterpriseMachineTranslationEnginesResource,
    MachineTranslationEnginesResource,
)
from .notifications.resource import NotificationResource
from .organization.resource import OrganizationResource
from .project_placeholders.resource import ProjectPlaceholdersResource
from .projects.resource import ProjectsResource
from .reports.resource import EnterpriseReportsResource, ReportsResource
from .screenshots.resource import ScreenshotsResource
from .security_logs.resource import SecurityLogsResource
from .source_files.resource import SourceFilesResource
from .source_strings.resource import EnterpriseSourceStringsResource, SourceStringsResource
from .storages.resource import StoragesResource
from .string_comments.resource import StringCommentsResource
from .string_corrections.resource import StringCorrectionsResource
from .string_translations.resource import StringTranslationsResource
from .style_guides.resource import StyleGuidesResource
from .system_placeholders.resource import SystemPlaceholdersResource
from .tasks.resource import EnterpriseTasksResource, TasksResource
from .teams.resource import TeamsResource
from .translation_memory.resource import TranslationMemoryResource
from .translation_status.resource import TranslationStatusResource
from .translations.resource import TranslationsResource
from .users.resource import EnterpriseUsersResource, UsersResource
from .vendors.resource import VendorsResource
from .webhooks.organization.resource import OrganizationWebhooksResource
from .webhooks.resource import WebhooksResource
from .workflows.resource import WorkflowsResource

__all__ = [
    "AdvisorsResource",
    "AIResource",
    "EnterpriseAIResource",
    "ApplicationResource",
    "BranchesResource",
    "BundlesResource",
    "ClientsResource",
    "CustomPlaceholdersResource",
    "CustomSpellcheckersResource",
    "DictionariesResource",
    "DistributionsResource",
    "ExternalQaChecksResource",
    "FieldsResource",
    "GlossariesResource",
    "GroupsResource",
    "LabelsResource",
    "LanguagesResource",
    "MachineTranslationEnginesResource",
    "EnterpriseMachineTranslationEnginesResource",
    "NotificationResource",
    "OrganizationResource",
    "OrganizationWebhooksResource",
    "ProjectPlaceholdersResource",
    "ProjectsResource",
    "ReportsResource",
    "EnterpriseReportsResource",
    "ScreenshotsResource",
    "SecurityLogsResource",
    "SourceFilesResource",
    "SourceStringsResource",
    "EnterpriseSourceStringsResource",
    "StoragesResource",
    "StringCommentsResource",
    "StringCorrectionsResource",
    "StringTranslationsResource",
    "StyleGuidesResource",
    "SystemPlaceholdersResource",
    "TasksResource",
    "EnterpriseTasksResource",
    "TeamsResource",
    "TranslationMemoryResource",
    "TranslationsResource",
    "TranslationStatusResource",
    "UsersResource",
    "EnterpriseUsersResource",
    "VendorsResource",
    "WebhooksResource",
    "WorkflowsResource",
]
