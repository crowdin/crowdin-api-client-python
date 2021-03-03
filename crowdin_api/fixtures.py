import pytest


@pytest.fixture()
def base_absolut_url():
    return "https://api.crowdin.com/api/v2/"


@pytest.fixture()
def base_url():
    return "api.crowdin.com/api/v2/"
