from typing import Optional

from crowdin_api.api_resources.abstract.resources import BaseResource


class CustomSpellcheckersResource(BaseResource):
    """
    Resource for Custom Spellcheckers.

    Crowdin Enterprise only.

    Link to documentation:
    https://support.crowdin.com/developer/enterprise/api/v2/#tag/Custom-Spellcheckers
    """

    def get_custom_spellcheckers_path(self, customSpellcheckerId: Optional[int] = None):
        if customSpellcheckerId is not None:
            return f"custom-spellcheckers/{customSpellcheckerId}"

        return "custom-spellcheckers"

    def list_custom_spellcheckers(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Custom Spellcheckers.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-spellcheckers.getMany
        """
        return self._get_entire_data(
            method="get",
            path=self.get_custom_spellcheckers_path(),
            params=self.get_page_params(offset=offset, limit=limit),
        )

    def get_custom_spellchecker(self, customSpellcheckerId: int):
        """
        Get Custom Spellchecker.

        Link to documentation:
        https://support.crowdin.com/developer/enterprise/api/v2/#operation/api.custom-spellcheckers.get
        """
        return self.requester.request(
            method="get",
            path=self.get_custom_spellcheckers_path(customSpellcheckerId=customSpellcheckerId),
        )
