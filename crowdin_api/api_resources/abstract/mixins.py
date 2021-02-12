from typing import Union, Optional


class RetrieveResourceMixin:
    def retrieve(self, object_id: Union[int, str]):
        return self.requester.request(method="get", path=self.prepare_path(object_id=object_id))


class ListResourceMixin:
    # page_size: int = 20

    def list(self, params: Optional[dict] = None, page: Optional[int] = None):
        # if page is not None:
        #     if page < 1:
        #         raise ValueError("The page number must be greater than or equal to 1.")
        #
        #     # todo: generate params

        return self.requester.request(method="get", path=self.prepare_path(), params=params)


class CreateResourceMixin:
    def create(self, data: dict):
        return self.requester.request(method="post", path=self.prepare_path(), post_data=data)


class EditResourceMixin:
    def update(self, object_id: Union[int, str], data: dict):
        return self.requester.request(
            method="put", path=self.prepare_path(object_id), post_data=data
        )


class DeleteResourceMixin:
    def retrieve(self, object_id):
        return self.requester.request(method="delete", path=self.prepare_path(object_id))


class BaseCRUDResourceMixin(
    ListResourceMixin,
    RetrieveResourceMixin,
    CreateResourceMixin,
    EditResourceMixin,
    DeleteResourceMixin,
):
    pass
