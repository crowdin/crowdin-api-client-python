from typing import Optional, Iterable, Union

from crowdin_api.api_resources.abstract.resources import BaseResource
from crowdin_api.api_resources.fields.enums import FieldEntity, FieldType
from crowdin_api.api_resources.fields.types import (
    ListFieldConfig,
    NumberFieldConfig,
    OtherFieldConfig,
    FieldPatchRequest,
)


class FieldsResource(BaseResource):
    """
    Resource for Fields.

    Link to documentation:
    https://developer.crowdin.com/enterprise/api/v2/#tag/Fields
    """

    def get_fields_path(self, fieldId: Optional[int] = None):
        if fieldId is None:
            return "fields"
        return f"fields/{fieldId}"

    def list_fields(
        self,
        search: Optional[str] = None,
        entity: Optional[FieldEntity] = None,
        type: Optional[FieldType] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ):
        """
        List Fields

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.fields.getMany
        """
        params = {"search": search, "entity": entity, "type": type}
        params.update(self.get_page_params(limit=limit, offset=offset))

        return self._get_entire_data(
            method="get", path=self.get_fields_path(), params=params
        )

    def add_field(
        self,
        name: str,
        slug: str,
        type: FieldType,
        entities: Iterable[FieldEntity],
        description: Optional[str] = None,
        config: Optional[
            Union[ListFieldConfig, NumberFieldConfig, OtherFieldConfig]
        ] = None,
    ):
        """
        Add Field

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.fields.post
        """
        data = {
            "name": name,
            "slug": slug,
            "type": type,
            "entities": entities,
            "description": description,
            "config": config,
        }

        return self.requester.request(
            method="post", path=self.get_fields_path(), request_data=data
        )

    def get_field(self, fieldId: int):
        """
        Get Field

        Link to documentaion:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.fields.get
        """

        return self.requester.request(
            method="get", path=self.get_fields_path(fieldId=fieldId)
        )

    def delete_field(self, fieldId: int):
        """
        Delete Field

        Link to documetation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.fields.delete
        """

        return self.requester.request(
            method="delete", path=self.get_fields_path(fieldId=fieldId)
        )

    def edit_field(self, fieldId: int, data: Iterable[FieldPatchRequest]):
        """
        Edit Field

        Link to documentation:
        https://developer.crowdin.com/enterprise/api/v2/#operation/api.fields.patch
        """

        return self.requester.request(
            method="patch",
            path=self.get_fields_path(fieldId=fieldId),
            request_data=data,
        )
