from unittest import mock

from crowdin_api.api_resources.abstract.mixins import (
    RetrieveResourceMixin,
    CreateResourceMixin,
    EditResourceMixin,
    DeleteResourceMixin,
    ListResourceMixin,
)
from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.requester import APIRequester


@mock.patch("crowdin_api.requester.APIRequester.request")
def test_retrieve_resource_mixin(m_request, base_absolut_url):
    m_request.return_value = "retrieve"
    object_id = 1

    class TestResource(BaseResource, RetrieveResourceMixin):
        base_path = "test"

    resource = TestResource(requester=APIRequester(base_url=base_absolut_url))
    assert resource.retrieve(object_id=object_id) == m_request.return_value
    m_request.assert_called_once_with(method="get", path=resource.prepare_path(object_id=object_id))


@mock.patch("crowdin_api.requester.APIRequester.request")
def test_list_resource_mixin(m_request, base_absolut_url):
    m_request.return_value = "retrieve"
    params = {"key": "value"}

    class TestResource(BaseResource, ListResourceMixin):
        base_path = "test"

    resource = TestResource(requester=APIRequester(base_url=base_absolut_url))
    assert resource.list(params=params) == m_request.return_value
    m_request.assert_called_once_with(method="get", path=resource.prepare_path(), params=params)


@mock.patch("crowdin_api.requester.APIRequester.request")
def test_create_resource_mixin(m_request, base_absolut_url):
    m_request.return_value = "create"
    data = {"key": "value"}

    class TestResource(BaseResource, CreateResourceMixin):
        base_path = "test"

    resource = TestResource(requester=APIRequester(base_url=base_absolut_url))
    assert resource.create(data=data) == m_request.return_value
    m_request.assert_called_once_with(method="post", path=resource.prepare_path(), post_data=data)


@mock.patch("crowdin_api.requester.APIRequester.request")
def test_edit_resource_mixin(m_request, base_absolut_url):
    m_request.return_value = "edit"
    data = {"key": "value"}
    object_id = 1

    class TestResource(BaseResource, EditResourceMixin):
        base_path = "test"

    resource = TestResource(requester=APIRequester(base_url=base_absolut_url))
    assert resource.update(data=data, object_id=object_id) == m_request.return_value
    m_request.assert_called_once_with(
        method="put", path=resource.prepare_path(object_id=object_id), post_data=data
    )


@mock.patch("crowdin_api.requester.APIRequester.request")
def test_delete_resource_mixin(m_request, base_absolut_url):
    m_request.return_value = "delete"
    object_id = 1

    class TestResource(BaseResource, DeleteResourceMixin):
        base_path = "test"

    resource = TestResource(requester=APIRequester(base_url=base_absolut_url))
    assert resource.retrieve(object_id=object_id) == m_request.return_value
    m_request.assert_called_once_with(
        method="delete", path=resource.prepare_path(object_id=object_id)
    )
