from typing import Any, Iterable, List, Union, Dict

from crowdin_api.api_resources.enums import PatchOperation
from crowdin_api.api_resources.projects.enums import (
    ProjectPatchPath,
    EscapeQuotes,
    EscapeSpecialCharacters,
    ProjectFilePatchPath,
)
from crowdin_api.typing import TypedDict


class ProjectPatchRequest(TypedDict):
    value: Any
    op: PatchOperation
    path: ProjectPatchPath


class NotificationSettings(TypedDict):
    translatorNewStrings: bool
    managerNewStrings: bool
    managerLanguageCompleted: bool


class QACheckCategories(TypedDict):
    EMPTY: bool
    SIZE: bool
    TAGS: bool
    SPACES: bool
    VARIABLES: bool
    PUNCTUATION: bool
    SYMBOLREGISTER: bool
    SPECIALSYMBOLS: bool
    WRONGTRANSLATION: bool
    SPELLCHECK: bool
    ICU: bool
    TERMS: bool
    DUPLICATE: bool


class QAChecksIgnorableCategories(TypedDict):
    EMPTY: bool
    SIZE: bool
    TAGS: bool
    SPACES: bool
    VARIABLES: bool
    PUNCTUATION: bool
    SYMBOLREGISTER: bool
    SPECIALSYMBOLS: bool
    WRONGTRANSLATION: bool
    SPELLCHECK: bool
    ICU: bool
    TERMS: bool
    DUPLICATE: bool
    FTL: bool
    ANDROID: bool


class PropertyFileFormatSettings(TypedDict):
    escapeQuotes: EscapeQuotes
    escapeSpecialCharacters: EscapeSpecialCharacters
    exportPattern: str


class XmlFileFormatSettings(TypedDict):
    translateContent: bool
    translateAttributes: bool
    translatableElements: Iterable[str]
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str


class SpecificFileFormatSettings(TypedDict):
    """
    Includes kind standard file format settings:
        - WebXml file
        - Html file
        - Adoc file
        - Md file
        - FmMd file
        - FmHtml file
        - MadcapFisnp file
        - Idml file
        - Mif file
        - Dita file
    """
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str


class DocxFileFormatSettings(TypedDict):
    cleanTagsAggressively: bool
    translateHiddenText: bool
    translateHyperlinkUrls: bool
    translateHiddenRowsAndColumns: bool
    importNotes: bool
    importHiddenSlides: bool
    contentSegmentation: bool
    srxStorageId: int
    exportPattern: str


class MediaWikiFileFormatSettings(TypedDict):
    srxStorageId: int
    exportPattern: str


class TxtFileFormatSettings(TypedDict):
    srxStorageId: int
    exportPattern: str


class OtherFileFormatSettings(TypedDict):
    exportPattern: str


class AndroidStringsExporterSettings(TypedDict):
    convertPlaceholders: bool


class MacOSXStringsExporterSettings(TypedDict):
    convertPlaceholders: bool


class XliffStringsExporterSettings(TypedDict):
    languagePairMapping: Dict[str, str]


class ProjectFilePatchRequest(TypedDict):
    value: Union[str, List[str]]
    op: PatchOperation
    path: ProjectFilePatchPath
