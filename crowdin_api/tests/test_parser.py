import datetime
from enum import Enum

import pytest
from crowdin_api.parser import dumps, loads
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


@pytest.mark.parametrize(
    "in_value, out_value",
    (
        ('{"int": 1}', {"int": 1}),
        ('{"float": 3.14}', {"float": 3.14}),
        ('{"string": "some string"}', {"string": "some string"}),
        (
            '{"datetime": "1988-01-04T18:20:00+02:00"}',
            {
                "datetime": datetime.datetime(
                    year=1988,
                    month=1,
                    day=4,
                    hour=18,
                    minute=20,
                    second=0,
                    tzinfo=datetime.timezone(datetime.timedelta(minutes=60 * 2), "+0200"),
                )
            },
        ),
        (
            '{"datetime": "1988-01-04T18:20:00+02:30"}',
            {
                "datetime": datetime.datetime(
                    year=1988,
                    month=1,
                    day=4,
                    hour=18,
                    minute=20,
                    second=0,
                    tzinfo=datetime.timezone(datetime.timedelta(minutes=60 * 2 + 30), "+0230"),
                )
            },
        ),
        (
            '{"datetime": "1988-01-04T18:20:00-02:00"}',
            {
                "datetime": datetime.datetime(
                    year=1988,
                    month=1,
                    day=4,
                    hour=18,
                    minute=20,
                    second=0,
                    tzinfo=datetime.timezone(datetime.timedelta(minutes=-60 * 2), "-0200"),
                )
            },
        ),
        (
            '{"datetime": "1988-01-04T18:20:00-02:30"}',
            {
                "datetime": datetime.datetime(
                    year=1988,
                    month=1,
                    day=4,
                    hour=18,
                    minute=20,
                    second=0,
                    tzinfo=datetime.timezone(datetime.timedelta(minutes=-60 * 2 - 30), "-0230"),
                )
            },
        ),
    ),
)
def test_parser(in_value, out_value):
    load_result = loads(in_value)
    assert load_result == out_value

    dumps_result = dumps(load_result)
    assert dumps_result == in_value


class TestEnum(Enum):
    ID = "id"
    CREATED_AT = "createdAt"


def test_sorting_serialization():
    sorting = Sorting(
        [
            SortingRule(TestEnum.ID, SortingOrder.DESC),
            SortingRule(TestEnum.CREATED_AT, SortingOrder.ASC),
        ]
    )

    result = dumps({"orderBy": sorting})
    expected = '{"orderBy": "id desc,createdAt asc"}'

    assert result == expected
