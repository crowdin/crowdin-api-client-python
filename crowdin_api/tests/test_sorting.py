import pytest
from crowdin_api.sorting import SortingOrder, SortingRule, Sorting
from enum import Enum


class TestOrderBy(Enum):
    TEST = "test"
    OTHER = "other"
    LAST = "last"


class TestSorting:
    def test_sorting_order_str(self):
        assert str(SortingOrder.ASC) == "asc"
        assert str(SortingOrder.DESC) == "desc"

    def test_sorting_order_equality(self):
        assert SortingOrder.ASC == SortingOrder.ASC
        assert SortingOrder.ASC != SortingOrder.DESC
        assert SortingOrder.ASC != "asc"

    def test_sorting_rule_creation(self):
        rule = SortingRule(TestOrderBy.TEST)
        assert str(rule) == "test"

        rule_with_order = SortingRule(TestOrderBy.TEST, SortingOrder.ASC)
        assert str(rule_with_order) == "test asc"

    def test_sorting_rule_validation(self):
        with pytest.raises(ValueError, match="Rule must be of type Enum"):
            SortingRule("not_enum")

        with pytest.raises(ValueError, match="Rule cannot be of type SortingOrder"):
            SortingRule(SortingOrder.ASC)

        with pytest.raises(ValueError, match="Order must be of type SortingOrder"):
            SortingRule(TestOrderBy.TEST, "asc")

        class EmptyEnum(Enum):
            EMPTY = ""

        with pytest.raises(ValueError, match="Rule value cannot be empty"):
            SortingRule(EmptyEnum.EMPTY)

    def test_sorting_rule_equality(self):
        rule1 = SortingRule(TestOrderBy.TEST, SortingOrder.ASC)
        rule2 = SortingRule(TestOrderBy.TEST, SortingOrder.ASC)
        rule3 = SortingRule(TestOrderBy.OTHER, SortingOrder.ASC)

        assert rule1 == rule2
        assert rule1 != rule3
        assert rule1 != "test asc"

    def test_sorting_multiple_rules(self):
        rules = [
            SortingRule(TestOrderBy.TEST, SortingOrder.ASC),
            SortingRule(TestOrderBy.OTHER, SortingOrder.DESC),
        ]
        sorting = Sorting(rules)
        assert str(sorting) == "test asc,other desc"

    def test_sorting_multiple_rules_two(self):
        rules = [
            SortingRule(TestOrderBy.TEST, SortingOrder.ASC),
            SortingRule(TestOrderBy.OTHER),
            SortingRule(TestOrderBy.LAST, SortingOrder.DESC),
        ]
        sorting = Sorting(rules)
        assert str(sorting) == "test asc,other,last desc"

    def test_sorting_equality(self):
        rules1 = [SortingRule(TestOrderBy.TEST)]
        rules2 = [SortingRule(TestOrderBy.TEST)]
        rules3 = [SortingRule(TestOrderBy.OTHER)]

        sort1 = Sorting(rules1)
        sort2 = Sorting(rules2)
        sort3 = Sorting(rules3)

        assert sort1 == sort2
        assert sort1 != sort3
        assert sort1 != "test"
