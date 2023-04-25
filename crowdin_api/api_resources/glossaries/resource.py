from typing import Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.glossaries.enums import (
    TermPartOfSpeech,
    TermStatus,
    TermType,
    TermGender,
)
from crowdin_api.api_resources.glossaries.types import (
    GlossaryPatchRequest,
    TermPatchRequest,
    LanguagesDetails,
    GlossarySchemaRequest,
)


class GlossariesResource(BaseResource):
    """
    Resource for Glossaries.

    Glossaries help to explain some specific terms or the ones often used in the project so that
    they can be properly and consistently translated.

    Use API to manage glossaries or specific terms. Glossary export and import are asynchronous
    operations and shall be completed with sequence of API methods.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Glossaries
    """

    # Glossaries
    def get_glossaries_path(self, glossaryId: Optional[int] = None):
        if glossaryId is not None:
            return f"glossaries/{glossaryId}"

        return "glossaries"

    def list_glossaries(
        self,
        groupId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Glossaries.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.getMany
        """

        params = {"groupId": groupId}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_glossaries_path(),
            params=params,
        )

    def add_glossary(self, name: str, languageId: str):
        """
        Add Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.post
        """

        return self.requester.request(
            method="post",
            path=self.get_glossaries_path(),
            request_data={"name": name, "languageId": languageId},
        )

    def get_glossary(self, glossaryId: int):
        """
        Get Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.get
        """

        return self.requester.request(
            method="get",
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    def delete_glossary(self, glossaryId: int):
        """
        Delete Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    def edit_glossary(self, glossaryId: int, data: Iterable[GlossaryPatchRequest]):
        """
        Edit Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.patch
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

    def export_glossary(self, glossaryId: int, data: Optional[GlossarySchemaRequest] = None):
        """
        Export Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.exports.post
        """

        return self.requester.request(
            method="post",
            request_data=data,
            path=self.get_glossary_export_path(glossaryId=glossaryId),
        )

    def check_glossary_export_status(self, glossaryId: int, exportId: str):
        """
        Check Glossary Export Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.exports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_glossary_export_path(glossaryId=glossaryId, exportId=exportId),
        )

    def download_glossary(self, glossaryId: int, exportId: str):
        """
        Download Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.exports.download.download
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
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.imports.post
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
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.imports.get
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
        conceptId: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Terms.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.terms.getMany
        """

        params = {
            "userId": userId,
            "languageId": languageId,
            "conceptId": conceptId,
        }

        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
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
        status: Optional[TermStatus] = None,
        type: Optional[TermType] = None,
        gender: Optional[TermGender] = None,
        note: Optional[str] = None,
        url: Optional[str] = None,
        conceptId: Optional[int] = None,
    ):
        """
        Add Term.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.terms.post
        """

        return self.requester.request(
            method="post",
            path=self.get_terms_path(glossaryId=glossaryId),
            request_data={
                "languageId": languageId,
                "text": text,
                "description": description,
                "partOfSpeech": partOfSpeech,
                "status": status,
                "type": type,
                "gender": gender,
                "note": note,
                "url": url,
                "conceptId": conceptId
            },
        )

    def clear_glossary(
        self,
        glossaryId: int,
        languageId: Optional[str] = None,
        conceptId: Optional[int] = None,
    ):
        """
        Clear Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.terms.deleteMany
        """

        return self.requester.request(
            method="delete",
            path=self.get_terms_path(glossaryId=glossaryId),
            params={
                "languageId": languageId,
                "conceptId": conceptId,
            },
        )

    def get_term(self, glossaryId: int, termId: int):
        """
        Get Term.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.terms.get
        """

        return self.requester.request(
            method="get",
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def delete_term(self, glossaryId: int, termId: int):
        """
        Delete Term.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.terms.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def edit_term(self, glossaryId: int, termId: int, data: Iterable[TermPatchRequest]):
        """
        Edit Term.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.terms.patch
        """

        return self.requester.request(
            method="patch",
            request_data=data,
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def get_concepts_path(self, glossaryId: int, conceptId: Optional[int] = None):
        if conceptId is not None:
            return f"glossaries/{glossaryId}/concepts/{conceptId}"

        return f"glossaries/{glossaryId}/concepts"

    def list_concepts(
        self,
        glossaryId: int,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ):
        """
        List Concepts.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.concepts.getMany
        """

        return self._get_entire_data(
            method="get",
            path=self.get_concepts_path(glossaryId=glossaryId),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def get_concept(self, glossaryId: int, conceptId: int):
        """
        Get Concept.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.concepts.get
        """

        return self.requester.request(
            method="get",
            path=self.get_concepts_path(glossaryId=glossaryId, conceptId=conceptId),
        )

    def update_concept(
        self,
        glossaryId: int,
        conceptId: int,
        languagesDetails: Iterable[LanguagesDetails],
        subject: Optional[str] = None,
        definition: Optional[str] = None,
        note: Optional[str] = None,
        url: Optional[str] = None,
        figure: Optional[str] = None,
    ):
        """
        Get Concept.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.concepts.put
        """

        return self.requester.request(
            method="put",
            path=self.get_concepts_path(glossaryId=glossaryId, conceptId=conceptId),
            request_data={
                "languagesDetails": languagesDetails,
                "subject": subject,
                "definition": definition,
                "note": note,
                "url": url,
                "figure": figure,
            },
        )

    def delete_concept(self, glossaryId: int, conceptId: int):
        """
        Delete Concept.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.glossaries.concepts.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_concepts_path(glossaryId=glossaryId, conceptId=conceptId),
        )
