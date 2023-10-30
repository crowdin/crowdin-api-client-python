from unittest import mock


import pytest
from crowdin_api.api_resources import ApplicationResource
from crowdin_api.requester import APIRequester

class TestApplicationResource:
    resource_class = ApplicationResource

    def get_resource(self, base_absolut_url):
        return self.resource_class(requester=APIRequester(base_url=base_absolut_url))
    
    @pytest.mark.parametrize(
        "in_params, path",
        (
            ({"applicationIdentifier": "abc"}, "applications/abc/api"),
            ({"applicationIdentifier": "abc", "path": "test"}, "applications/abc/api/test"),
        ),
    )
    def test_get_applications_path(self, in_params, path, base_absolut_url):
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_path(**in_params) == path
    
    @mock.patch("crowdin_api.requester.APIRequester.request") 
    def  test_get_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_data(applicationIdentifier="abc", path="test") == "response"
        m_request.assert_called_once_with(
            method="get",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
        )
    @pytest.mark.parametrize(
       "in_params, request_data",
       (
           (
               {
                   "applicationIdentifier": "abc",
                   "path": "test"
               },
               {}
           )
       )  
     )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_add_application_data(self, m_request, in_params, request_data, base_absolut_url):
        m_request.return_value = "response"
        resource = self.get_resource(base_absolut_url)
        assert resource.add_application_data(applicationIdentifier="abc", path="test") == "response"
        m_request.assert_called_once_with(
            method="post",
            path=resource.aget_application_path(applicationIdentifier="abc", path="test"),
            request_data=request_data,
        )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_delete_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"

        resource = self.get_resource(base_absolut_url)
        assert resource.delete_application_data(applicationIdentifier="abc", path="test") == "response"
        m_request.assert_called_once_with(
            method="delete",
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
        )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_edit_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        data ={"key2":2}
        resource = self.get_resource(base_absolut_url)
        assert resource.get_application_data(applicationIdentifier="abc", path="test", data=data) == "response"
        m_request.assert_called_once_with(
            method="patch",
            data=data,
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
        )
    @mock.patch("crowdin_api.requester.APIRequester.request")
    def test_update_application_data(self, m_request, base_absolut_url):
        m_request.return_value = "response"
        data ={"key2":2}
        resource = self.get_resource(base_absolut_url)
        assert resource.update_application_data(applicationIdentifier="abc", path="test", data=data) == "response"
        m_request.assert_called_once_with(
            method="put",
            data=data,
            path=resource.get_application_path(applicationIdentifier="abc", path="test"),
        )
        