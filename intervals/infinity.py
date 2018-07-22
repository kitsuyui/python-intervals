from enum import Enum


class Infinity(Enum):
    Positive = object()
    Negative = object()

    def __lt__(self, other: object) -> bool:
        if self == other:
            return False
        if self == Infinity.Negative:
            return True
        return False

    def __gt__(self, other: object) -> bool:
        if self == other:
            return False
        if self == Infinity.Positive:
            return True
        return False

    def __le__(self, other: object) -> bool:
        return not self > other

    def __ge__(self, other: object) -> bool:
        return not self < other
