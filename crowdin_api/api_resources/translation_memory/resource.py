from typing import Dict, Iterable, Optional, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.enums import ExportFormat
from crowdin_api.api_resources.translation_memory.types import (
    TranslationMemoryPatchRequest,
    TranslationMemorySegmentRecord,
    TranslationMemorySegmentRecordOperationAdd,
    TranslationMemorySegmentRecordOperationReplace,
    TranslationMemorySegmentRecordOperationRemove,
)
from crowdin_api.sorting import Sorting


class TranslationMemoryResource(BaseResource):
    """
    Resource for Translation Memory.

    Translation Memory (TM) is a vault of translations that were previously made in other projects.
     Those translations can be reused to speed up the translation process. Every translation made
     in the project is automatically added to the project Translation Memory.

    Use API to create, upload, download, or remove specific TM. Translation Memory export and import
    are asynchronous operations and shall be completed with sequence of API methods.

    Link to documentation:
    https://developer.crowdin.com/api/v2/#tag/Translation-Memory
    """

    def get_tms_path(self, tmId: Optional[int] = None):
        if tmId is not None:
            return f"tms/{tmId}"

        return "tms"

    def list_tms(
        self,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List TMs.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.getMany
        """

        params = {"orderBy": orderBy}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_tms_path(),
            params=params,
        )

    def add_tm(self, name: str, languageId: str):
        """
        Add Glossary.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.post
        """

        return self.requester.request(
            method="post",
            path=self.get_tms_path(),
            request_data={"name": name, "languageId": languageId},
        )

    def get_tm(self, tmId: int):
        """
        Get TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.get
        """

        return self.requester.request(method="get", path=self.get_tms_path(tmId=tmId))

    def delete_tm(self, tmId: int):
        """
        Delete TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.delete
        """

        return self.requester.request(method="delete", path=self.get_tms_path(tmId=tmId))

    def edit_tm(self, tmId: int, data: Iterable[TranslationMemoryPatchRequest]):
        """
        Edit TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.patch
        """

        return self.requester.request(
            method="patch", request_data=data, path=self.get_tms_path(tmId=tmId)
        )

    def clear_tm(self, tmId: int):
        """
        Clear TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.segments.clear
        """

        return self.requester.request(
            method="delete", path=f"{self.get_tms_path(tmId=tmId)}/segments"
        )

    # TM Segments
    def get_tm_segments_path(self, tmId: int, segmentId: Optional[int] = None):
        if segmentId is None:
            return f"tms/{tmId}/segments"
        return f"tms/{tmId}/segments/{segmentId}"

    def list_tm_segments(
        self,
        tmId: int,
        orderBy: Optional[Sorting] = None,
        page: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        """
        List TM Segments.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.segments.getMany
        """
        params = {"orderBy": orderBy}
        params.update(self.get_page_params(page=page, offset=offset, limit=limit))

        return self._get_entire_data(
            method="get",
            path=self.get_tm_segments_path(tmId=tmId),
            params=params,
        )

    def create_tm_segment(
        self, tmId: int, records: Iterable[TranslationMemorySegmentRecord]
    ):
        """
        Create TM Segment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.segments.post
        """
        data = {"records": records}

        return self.requester.request(
            method="post",
            path=self.get_tm_segments_path(tmId=tmId),
            request_data=data,
        )

    def get_tm_segment(self, tmId: int, segmentId: int):
        """
        Get TM Segment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.segments.get
        """
        return self.requester.request(
            method="get", path=self.get_tm_segments_path(tmId=tmId, segmentId=segmentId)
        )

    def delete_tm_segment(self, tmId: int, segmentId: int):
        """
        Delete TM Segment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.segments.delete
        """
        return self.requester.request(
            method="delete",
            path=self.get_tm_segments_path(tmId=tmId, segmentId=segmentId)
        )

    def edit_tm_segment(
        self,
        tmId: int,
        segmentId: int,
        data: Iterable[
            Union[
                TranslationMemorySegmentRecordOperationAdd,
                TranslationMemorySegmentRecordOperationReplace,
                TranslationMemorySegmentRecordOperationRemove,
            ]
        ],
    ):
        """
        Edit TM Segment.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.segments.patch
        """
        return self.requester.request(
            method="patch",
            path=self.get_tm_segments_path(tmId=tmId, segmentId=segmentId),
            request_data=data,
        )

    # Export
    def get_tm_export_path(self, tmId: int, exportId: Optional[str] = None):
        if exportId is not None:
            return f"tms/{tmId}/exports/{exportId}"

        return f"tms/{tmId}/exports"

    def export_tm(
        self,
        tmId: int,
        sourceLanguageId: Optional[str] = None,
        targetLanguageId: Optional[str] = None,
        format: Optional[ExportFormat] = None,
    ):
        """
        Export TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.exports.post
        """

        return self.requester.request(
            method="post",
            request_data={
                "sourceLanguageId": sourceLanguageId,
                "targetLanguageId": targetLanguageId,
                "format": format,
            },
            path=self.get_tm_export_path(tmId=tmId),
        )

    def check_tm_export_status(self, tmId: int, exportId: str):
        """
        Check TM Export Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.exports.get
        """

        return self.requester.request(
            method="get", path=self.get_tm_export_path(tmId=tmId, exportId=exportId)
        )

    def download_tm(self, tmId: int, exportId: str):
        """
        Download TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.exports.download.download
        """

        return self.requester.request(
            method="get",
            path=f"{self.get_tm_export_path(tmId=tmId, exportId=exportId)}/download",
        )

    def concordance_search_in_tms(
        self,
        sourceLanguageId: str,
        targetLanguageId: str,
        autoSubstitution: bool,
        minRelevant: int,
        expressions: Iterable[str],
        projectId: Optional[int] = None,
    ):
        """
        Concordance search in TMs

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.projects.tms.concordance.post
        """

        projectId = projectId or self.get_project_id()
        data = {
            "sourceLanguageId": sourceLanguageId,
            "targetLanguageId": targetLanguageId,
            "autoSubstitution": autoSubstitution,
            "minRelevant": minRelevant,
            "expressions": expressions,
        }

        return self.requester.request(
            method="post",
            path=f"projects/{projectId}/tms/concordance",
            request_data=data,
        )

    # Import
    def import_tm(
        self,
        tmId: int,
        storageId: int,
        scheme: Optional[Dict] = None,
        firstLineContainsHeader: Optional[bool] = None,
    ):
        """
        Import TM.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.imports.post
        """

        return self.requester.request(
            method="post",
            request_data={
                "storageId": storageId,
                "scheme": scheme,
                "firstLineContainsHeader": firstLineContainsHeader,
            },
            path=f"{self.get_tms_path(tmId=tmId)}/imports",
        )

    def check_tm_import_status(self, tmId: int, importId: str):
        """
        Check TM Import Status.

        Link to documentation:
        https://developer.crowdin.com/api/v2/#operation/api.tms.imports.get
        """

        return self.requester.request(
            method="get", path=f"{self.get_tms_path(tmId=tmId)}/imports/{importId}"
        )
