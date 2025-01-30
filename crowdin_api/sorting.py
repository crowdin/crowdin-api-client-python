from enum import Enum
from typing import Optional, List


class SortingOrder(Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, SortingOrder):
            return self.value == other.value
        return False


class SortingRule:
    def __init__(self, rule: Enum, order: Optional[SortingOrder] = None):
        if not isinstance(rule, Enum):
            raise ValueError("Rule must be of type Enum.")
        if not rule.value:
            raise ValueError("Rule value cannot be empty.")
        if isinstance(rule, SortingOrder):
            raise ValueError("Rule cannot be of type SortingOrder.")
        if order and not isinstance(order, SortingOrder):
            raise ValueError("Order must be of type SortingOrder.")

        self.rule = rule.value
        self.order = order

    def __str__(self):
        return f"{self.rule} {self.order}" if self.order else self.rule

    def __eq__(self, other):
        if not isinstance(other, SortingRule):
            return False
        return self.rule == other.rule and self.order == other.order


class Sorting:
    def __init__(self, rules: List[SortingRule]):
        self.rules = rules

    def __str__(self):
        return ",".join([str(rule) for rule in self.rules])

    def __eq__(self, other):
        if not isinstance(other, Sorting):
            return False
        return self.rules == other.rules
