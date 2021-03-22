from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import ExportFormat
from crowdin_api.api_resources.glossaries.enums import TermPartOfSpeech
from crowdin_api.api_resources.glossaries.types import GlossaryPatchRequest, TermPatchRequest


class GlossariesResource(BaseResource):
    """
    Resource for Glossaries.

    Glossaries help to explain some specific terms or the ones often used in the project so that
    they can be properly and consistently translated.

    Use API to manage glossaries or specific terms. Glossary export and import are asynchronous
    operations and shall be completed with sequence of API methods.

    Link to documentation:
    https://support.crowdin.com/api/v2/#tag/Glossaries
    """

    # Glossaries
    def get_glossaries_path(self, glossaryId: Optional[int] = None):
        if glossaryId is not None:
            return f"glossaries/{glossaryId}"

        return "glossaries"

    def list_glossaries(
        self,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Glossaries.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.getMany
        """

        return self.requester.request(
            method="get",
            path=self.get_glossaries_path(),
            params=self.get_page_params(page=page, offset=offset, limit=limit),
        )

    def add_glossary(self, name: str):
        """
        Add Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.post
        """

        return self.requester.request(
            method="post", path=self.get_glossaries_path(), request_data={"name": name}
        )

    def get_glossary(self, glossaryId: int):
        """
        Get Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.get
        """

        return self.requester.request(
            method="get",
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    def delete_glossary(self, glossaryId: int):
        """
        Delete Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    def edit_glossary(self, glossaryId: int, data: Iterable[GlossaryPatchRequest]):
        """
        Edit Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.patch
        """

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    # Export
    def get_glossary_export_path(self, glossaryId: int, exportId: Optional[str] = None):
        if exportId is not None:
            return f"glossaries/{glossaryId}/exports/{exportId}"

        return f"glossaries/{glossaryId}/exports"

    def export_glossary(self, glossaryId: int, format: Optional[ExportFormat] = None):
        """
        Export Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.exports.post
        """

        return self.requester.request(
            method="post",
            request_data={"format": format},
            path=self.get_glossary_export_path(glossaryId=glossaryId),
        )

    def check_glossary_export_status(self, glossaryId: int, exportId: str):
        """
        Check Glossary Export Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.exports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_glossary_export_path(glossaryId=glossaryId, exportId=exportId),
        )

    def download_glossary(self, glossaryId: int, exportId: str):
        """
        Download Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.exports.download.download
        """

        glossary_export_path = self.get_glossary_export_path(
            glossaryId=glossaryId, exportId=exportId
        )

        return self.requester.request(
            method="get",
            path=f"{glossary_export_path}/download",
        )

    # Import
    def import_glossary(
        self,
        glossaryId: int,
        storageId: int,
        scheme: Optional[Dict] = None,
        firstLineContainsHeader: Optional[bool] = None,
    ):
        """
        Import Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.imports.post
        """

        return self.requester.request(
            method="post",
            request_data={
                "storageId": storageId,
                "scheme": scheme,
                "firstLineContainsHeader": firstLineContainsHeader,
            },
            path=f"{self.get_glossaries_path(glossaryId=glossaryId)}/imports",
        )

    def check_glossary_import_status(self, glossaryId: int, importId: str):
        """
        Check Glossary Import Status.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.imports.get
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_glossaries_path(glossaryId=glossaryId)}/imports/{importId}",
        )

    # Terms
    def get_terms_path(self, glossaryId: int, termId: Optional[int] = None):
        if termId is not None:
            return f"glossaries/{glossaryId}/terms/{termId}"

        return f"glossaries/{glossaryId}/terms"

    def list_terms(
        self,
        glossaryId: int,
        userId: Optional[int] = None,
        languageId: Optional[str] = None,
        translationOfTermId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Terms.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.terms.getMany
        """

        params = {
            "userId": userId,
            "languageId": languageId,
            "translationOfTermId": translationOfTermId,
        }

        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self.requester.request(
            method="get",
            path=self.get_terms_path(glossaryId=glossaryId),
            params=params,
        )

    def add_term(
        self,
        glossaryId: int,
        languageId: str,
        text: str,
        description: Optional[str] = None,
        partOfSpeech: Optional[TermPartOfSpeech] = None,
        translationOfTermId: Optional[int] = None,
    ):
        """
        Add Term.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.terms.post
        """

        return self.requester.request(
            method="post",
            path=self.get_terms_path(glossaryId=glossaryId),
            request_data={
                "languageId": languageId,
                "text": text,
                "description": description,
                "partOfSpeech": partOfSpeech,
                "translationOfTermId": translationOfTermId,
            },
        )

    def clear_glossary(
        self,
        glossaryId: int,
        languageId: Optional[str] = None,
        translationOfTermId: Optional[int] = None,
    ):
        """
        Clear Glossary.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.terms.deleteMany
        """

        return self.requester.request(
            method="delete",
            path=self.get_terms_path(glossaryId=glossaryId),
            params={
                "languageId": languageId,
                "translationOfTermId": translationOfTermId,
            },
        )

    def get_term(self, glossaryId: int, termId: int):
        """
        Get Term.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.terms.get
        """

        return self.requester.request(
            method="get",
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def delete_term(self, glossaryId: int, termId: int):
        """
        Delete Term.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.terms.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def edit_term(self, glossaryId: int, termId: int, data: Iterable[TermPatchRequest]):
        """
        Edit Term.

        Link to documentation:
        https://support.crowdin.com/api/v2/#operation/api.glossaries.terms.patch
        """

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )
