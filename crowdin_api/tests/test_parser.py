import datetime
from enum import Enum

import pytest
from crowdin_api.parser import dumps, loads
from crowdin_api.sorting import Sorting, SortingOrder, SortingRule


class TestEnum(Enum):
    ONE = "one"
    TWO = "two"


@pytest.mark.parametrize(
    "in_value, out_value",
    (
        (
            '{"orderBy": "one desc,two"}',
            {
                "orderBy": str(
                    Sorting(
                        [
                            SortingRule(TestEnum.ONE, SortingOrder.DESC),
                            SortingRule(TestEnum.TWO),
                        ]
                    )
                )
            },
        ),
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
