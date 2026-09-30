from typing import Any, Dict, Iterable, Optional

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.glossaries.enums import (
    TermGender,
    TermPartOfSpeech,
    TermStatus,
    TermType,
)
from crowdin_api.api_resources.glossaries.types import (
    GlossaryPatchRequest,
    GlossarySchemaRequest,
    LanguagesDetails,
    OrganizationConcordanceSearchRequest,
    TermPatchRequest,
)
from crowdin_api.sorting import Sorting


class GlossariesResource(BaseResource):
    """
    Resource for Glossaries.

    Glossaries help to explain some specific terms or the ones often used in the project so that
    they can be properly and consistently translated.

    Use API to manage glossaries or specific terms. Glossary export and import are asynchronous
    operations and shall be completed with sequence of API methods.

    Link to documentation:
    https://support.crowdin.com/developer/api/v2/#tag/Glossaries
    """

    # Glossaries
    def get_glossaries_path(self, glossaryId: Optional[int] = None):
        if glossaryId is not None:
            return f"glossaries/{glossaryId}"

        return "glossaries"

    def list_glossaries(
        self,
        orderBy: Optional[Sorting] = None,
        groupId: Optional[int] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        userId: Optional[int] = None,
        filter: Optional[str] = None,
    ):
        """
        List Glossaries.

        :param groupId: Group Identifier. Set 0 to see glossaries of root group.
            Crowdin Enterprise only.
        :param userId: List user glossaries. Crowdin only.
        :param filter: Filter glossaries by `name`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.getMany
        """

        params = {"orderBy": orderBy, "groupId": groupId, "userId": userId, "filter": filter}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_glossaries_path(),
            params=params,
        )

    def add_glossary(
        self,
        name: str,
        languageId: str,
        isShared: Optional[bool] = None,
        groupId: Optional[int] = None,
    ):
        """
        Add Glossary.

        :param isShared: Whether the glossary should be shared to all projects within the account
            (Crowdin) or within the group (Crowdin Enterprise).
        :param groupId: Group Identifier. If 0 – the glossary will be available for all projects
            and groups in the workspace. Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.post
        """

        return self.requester.request(
            method="post",
            path=self.get_glossaries_path(),
            request_data={
                "name": name,
                "languageId": languageId,
                "isShared": isShared,
                "groupId": groupId,
            },
        )

    def get_glossary(self, glossaryId: int):
        """
        Get Glossary.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.get
        """

        return self.requester.request(
            method="get",
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    def delete_glossary(self, glossaryId: int):
        """
        Delete Glossary.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_glossaries_path(glossaryId=glossaryId),
        )

    def edit_glossary(self, glossaryId: int, data: Iterable[GlossaryPatchRequest]):
        """
        Edit Glossary.

        `GlossaryPatchPath.GROUP_ID` (`/groupId`) is Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.patch
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
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.exports.post
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
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.exports.get
        """

        return self.requester.request(
            method="get",
            path=self.get_glossary_export_path(glossaryId=glossaryId, exportId=exportId),
        )

    def download_glossary(self, glossaryId: int, exportId: str):
        """
        Download Glossary.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.exports.download.download
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
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.imports.post
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
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.imports.get
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_glossaries_path(glossaryId=glossaryId)}/imports/{importId}",
        )

    def concordance_search_in_glossaries(
        self,
        sourceLanguageId: str,
        targetLanguageId: str,
        expressions: Iterable[str],
        projectId: Optional[int] = None,
    ):
        """
        Concordance search in Glossaries

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.projects.glossaries.concordance.post
        """
        data = {
            "sourceLanguageId": sourceLanguageId,
            "targetLanguageId": targetLanguageId,
            "expressions": expressions,
        }

        projectId = projectId or self.get_project_id()

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/glossaries/concordance",
            request_data=data,
        )

    def organization_concordance_search(self, request_data: OrganizationConcordanceSearchRequest):
        """
        Concordance search in organization glossaries.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.concordance.post

        Link to documentation for enterprise:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.glossaries.concordance.post
        """

        return self.requester.request(
            method="post",
            path="glossaries/concordance",
            request_data=request_data,
        )

    # Terms
    def get_terms_path(self, glossaryId: int, termId: Optional[int] = None):
        if termId is not None:
            return f"glossaries/{glossaryId}/terms/{termId}"

        return f"glossaries/{glossaryId}/terms"

    def list_terms(
        self,
        glossaryId: int,
        orderBy: Optional[Sorting] = None,
        userId: Optional[int] = None,
        languageId: Optional[str] = None,
        conceptId: Optional[int] = None,
        croql: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        translationOfTermId: Optional[int] = None,
    ):
        """
        List Terms.

        :param translationOfTermId: Filter terms by `termId`. Use for terms that have translations.
        :param croql: Filter terms by CroQL. Can be used only with `orderBy`, `offset` and `limit`.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.terms.getMany
        """

        params = {
            "orderBy": orderBy,
            "userId": userId,
            "languageId": languageId,
            "conceptId": conceptId,
            "translationOfTermId": translationOfTermId,
            "croql": croql,
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
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Add Term.

        :param conceptId: Defines whether to add translation to the existing term. If not
            specified, a new concept will be automatically created for the term.
        :param fields: Custom fields values. Keys get via List Fields. Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.terms.post
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
                "conceptId": conceptId,
                "fields": fields,
            },
        )

    def clear_glossary(
        self,
        glossaryId: int,
        languageId: Optional[str] = None,
        conceptId: Optional[int] = None,
        translationOfTermId: Optional[int] = None,
    ):
        """
        Clear Glossary.

        Without a filter every term is deleted.

        :param translationOfTermId: Defines whether to delete specific term along with its
            translations.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.terms.deleteMany
        """

        return self.requester.request(
            method="delete",
            path=self.get_terms_path(glossaryId=glossaryId),
            params={
                "languageId": languageId,
                "conceptId": conceptId,
                "translationOfTermId": translationOfTermId,
            },
        )

    def get_term(self, glossaryId: int, termId: int):
        """
        Get Term.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.terms.get
        """

        return self.requester.request(
            method="get",
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def delete_term(self, glossaryId: int, termId: int):
        """
        Delete Term.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.terms.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_terms_path(glossaryId=glossaryId, termId=termId),
        )

    def edit_term(self, glossaryId: int, termId: int, data: Iterable[TermPatchRequest]):
        """
        Edit Term.

        `TermPatchPath.FIELDS` (`/fields`) is Crowdin Enterprise only. A `replace` on `/fields`
        writes the whole set of custom field values.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.terms.patch
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
        orderBy: Optional[Sorting] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List Concepts.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.concepts.getMany
        """

        params = {"orderBy": orderBy}
        params.update(self.get_page_params(offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_concepts_path(glossaryId=glossaryId),
            params=params,
        )

    def get_concept(self, glossaryId: int, conceptId: int):
        """
        Get Concept.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.concepts.get
        """

        return self.requester.request(
            method="get",
            path=self.get_concepts_path(glossaryId=glossaryId, conceptId=conceptId),
        )

    def update_concept(
        self,
        glossaryId: int,
        conceptId: int,
        languagesDetails: Optional[Iterable[LanguagesDetails]] = None,
        subject: Optional[str] = None,
        definition: Optional[str] = None,
        note: Optional[str] = None,
        url: Optional[str] = None,
        figure: Optional[str] = None,
        translatable: Optional[bool] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        """
        Update Concept.

        :param fields: Custom fields values. Keys get via List Fields. Writes the whole set of
            custom field values. Crowdin Enterprise only.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.concepts.put
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
                "translatable": translatable,
                "fields": fields,
            },
        )

    def delete_concept(self, glossaryId: int, conceptId: int):
        """
        Delete Concept.

        Link to documentation:
        https://support.crowdin.com/developer/api/v2/#operation/api.glossaries.concepts.delete
        """

        return self.requester.request(
            method="delete",
            path=self.get_concepts_path(glossaryId=glossaryId, conceptId=conceptId),
        )
