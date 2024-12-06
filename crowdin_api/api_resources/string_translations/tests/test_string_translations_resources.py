from unittest import mock

import pytest
from crowdin_api.api_resources.enums import DenormalizePlaceholders
from crowdin_api.api_resources.string_translations.enums import (
    ListLanguageTranslationsOrderBy,
    ListStringTranslationsOrderBy,
    ListTranslationApprovalsOrderBy,
    VoteMark,
)
from crowdin_api.api_resources.string_translations.resource import StringTranslationsResource
from crowdin_api.requester import APIRequester
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestStringTranslationsResource:
    resource_class = StringTranslationsResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))

    def test_resource_with_id(self, base_absolut_url):
        project_id = 1
        resource = self.resource_class(
            requester=APIRequester(base_url=base_absolut_url), project_id=project_id
        )
        assert resource.get_project_id() == project_id

    # Approval
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/approvals"),
            ({"projectId": 1, "approvalId": 2}, "projects/1/approvals/2"),
        ),
    )
    def test_get_approvals_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_approvals_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "orderBy": None,
                    "offset": 0,
                    "limit": 10,
                    "fileId": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                    "stringId": None,
                    "languageId": None,
                    "translationId": None,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListTranslationApprovalsOrderBy.ID, SortingOrder.DESC
                            )
                        ]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "fileId": 1,
                    "labelIds": "1,2,3",
                    "excludeLabelIds": "4,5,6",
                    "stringId": 2,
                    "languageId": "ua",
                    "translationId": 3,
                },
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListTranslationApprovalsOrderBy.ID, SortingOrder.DESC
                            )
                        ]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "fileId": 1,
                    "labelIds": "1,2,3",
                    "excludeLabelIds": "4,5,6",
                    "stringId": 2,
                    "languageId": "ua",
                    "translationId": 3,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_translation_approvals(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_translation_approvals(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_approvals_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_approval(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_approval(projectId=1, translationId=2) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_approvals_path(projectId=1),
            request_data={"translationId": 2},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_remove_string_approvals(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        stringId = 1
        projectId = 2
        resource = self.get_resource(base_absolut_url)
        assert (
            resource.remove_string_approvals(stringId=stringId, projectId=projectId)
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_approvals_path(projectId=projectId),
            params={"stringId": stringId},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_approval(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_approval(projectId=1, approvalId=2) == "response"
        m_request.assert_called_once_with(
            method="get", path=resource.get_approvals_path(projectId=1, approvalId=2)
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_remove_approval(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.remove_approval(projectId=1, approvalId=2) == "response"
        m_request.assert_called_once_with(
            method="delete", path=resource.get_approvals_path(projectId=1, approvalId=2)
        )

    # Language Translations
    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "orderBy": None,
                    "offset": 0,
                    "limit": 10,
                    "stringIds": None,
                    "labelIds": None,
                    "fileId": None,
                    "branchId": None,
                    "directoryId": None,
                    "croql": None,
                    "denormalizePlaceholders": None,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListLanguageTranslationsOrderBy.TRANSLATION_ID,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "stringIds": [1, 2, 3],
                    "labelIds": [3, 4, 5],
                    "fileId": 5,
                    "branchId": 6,
                    "directoryId": 7,
                    "croql": "croql",
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                },
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListLanguageTranslationsOrderBy.TRANSLATION_ID,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "stringIds": "1,2,3",
                    "labelIds": "3,4,5",
                    "fileId": 5,
                    "branchId": 6,
                    "directoryId": 7,
                    "croql": "croql",
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_language_translations(
        self, m_request, in_params, request_params, base_absolut_url
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.list_language_translations(projectId=1, languageId="ua", **in_params)
            == "response"
        )
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path="projects/1/languages/ua/translations",
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_translation_alignment(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)

        data = {
            "sourceLanguageId": "en",
            "targetLanguageId": "de",
            "text": "Your password has been reset successfully!"
        }

        assert resource.translation_alignment(projectId=1, **data)
        m_request.assert_called_once_with(
            method="post",
            path="projects/1/translations/alignment",
            request_data=data,
        )

    # Translations
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/translations"),
            ({"projectId": 1, "translationId": 2}, "projects/1/translations/2"),
        ),
    )
    def test_get_translations_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_translations_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "orderBy": None,
                    "offset": 0,
                    "limit": 10,
                    "stringId": None,
                    "languageId": None,
                    "denormalizePlaceholders": None,
                },
            ),
            (
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListStringTranslationsOrderBy.ID,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "stringId": 1,
                    "languageId": 2,
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                },
                {
                    "orderBy": Sorting(
                        [
                            SortingRule(
                                ListStringTranslationsOrderBy.ID,
                                SortingOrder.DESC,
                            )
                        ]
                    ),
                    "offset": 0,
                    "limit": 10,
                    "stringId": 1,
                    "languageId": 2,
                    "denormalizePlaceholders": DenormalizePlaceholders.ENABLE,
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_string_translations(self, m_request, in_params, request_params, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_string_translations(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_translations_path(projectId=1),
        )

    @pytest.mark.parametrize(
        "in_params, request_data",
        (
            (
                {
                    "stringId": 1,
                    "languageId": "ua",
                    "text": "text",
                },
                {
                    "stringId": 1,
                    "languageId": "ua",
                    "text": "text",
                    "pluralCategoryName": None,
                },
            ),
            (
                {
                    "stringId": 1,
                    "languageId": "ua",
                    "text": "text",
                    "pluralCategoryName": "some name",
                },
                {
                    "stringId": 1,
                    "languageId": "ua",
                    "text": "text",
                    "pluralCategoryName": "some name",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_translation(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_translation(projectId=1, **request_data) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_translations_path(projectId=1),
            request_data=request_data,
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_string_translations(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert (
            resource.delete_string_translations(projectId=1, stringId=2, languageId="ua")
            == "response"
        )
        m_request.assert_called_once_with(
            method="delete",
            params={"stringId": 2, "languageId": "ua"},
            path=resource.get_translations_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_translation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_translation(projectId=1, translationId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_translations_path(projectId=1, translationId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_restore_translation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.restore_translation(projectId=1, translationId=2) == "response"
        m_request.assert_called_once_with(
            method="put",
            path=resource.get_translations_path(projectId=1, translationId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_translation(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_translation(projectId=1, translationId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_translations_path(projectId=1, translationId=2),
        )

    # Translation Votes
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"projectId": 1}, "projects/1/votes"),
            ({"projectId": 1, "voteId": 2}, "projects/1/votes/2"),
        ),
    )
    def test_get_translation_votes_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_translation_votes_path(**in_params) == path

    @pytest.mark.parametrize(
        "in_params, request_params",
        (
            (
                {"offset": 0, "limit": 10},
                {
                    "offset": 0,
                    "limit": 10,
                    "stringId": None,
                    "languageId": None,
                    "translationId": None,
                    "fileId": None,
                    "labelIds": None,
                    "excludeLabelIds": None,
                },
            ),
            (
                {
                    "offset": 0,
                    "limit": 10,
                    "stringId": 1,
                    "languageId": "ua",
                    "translationId": 2,
                    "fileId": 1,
                    "labelIds": "1,2,3",
                    "excludeLabelIds": "4,5,6",
                },
                {
                    "offset": 0,
                    "limit": 10,
                    "stringId": 1,
                    "languageId": "ua",
                    "translationId": 2,
                    "fileId": 1,
                    "labelIds": "1,2,3",
                    "excludeLabelIds": "4,5,6",
                },
            ),
        ),
    )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_list_translation_votes(
        self,
        m_request,
        in_params,
        request_params,
        base_absolut_url,
    ):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.list_translation_votes(projectId=1, **in_params) == "response"
        m_request.assert_called_once_with(
            method="get",
            params=request_params,
            path=resource.get_translation_votes_path(projectId=1),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_vote(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.add_vote(projectId=1, mark=VoteMark.UP, translationId=2) == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.get_translation_votes_path(projectId=1),
            request_data={"translationId": 2, "mark": VoteMark.UP},
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_get_vote(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_vote(projectId=1, voteId=2) == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_translation_votes_path(projectId=1, voteId=2),
        )

    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_cancel_vote(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.cancel_vote(projectId=1, voteId=2) == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_translation_votes_path(projectId=1, voteId=2),
        )
