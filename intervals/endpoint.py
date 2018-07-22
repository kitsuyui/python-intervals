from typing import cast, Generic, TypeVar, Union
from intervals.infinity import Infinity
from intervals.comparable import Comparable


T = TypeVar('T', bound=Comparable)


class Endpoint(Generic[T]):
    value: Union[T, Infinity]
    open: bool

    def __init__(self,
                 value: Union[T, Infinity],
                 *,
                 open: bool=False) -> None:
        self.value = value
        self.open = open

    def __eq__(self, other: object) -> bool:
        if type(self) != type(other):
            return False
        other = cast(Endpoint[T], other)
        return all((
            self.value == other.value,
            self.open == other.open,
        ))

    def __lt__(self, other: object) -> bool:
        if type(self) != type(other):
            other = Endpoint(cast(T, other))
        else:
            other = cast(Endpoint[T], other)
        if isinstance(other.value, Infinity):
            return other.value > self.value
        return self.value < other.value

    def __gt__(self, other: object) -> bool:
        if type(self) != type(other):
            other = Endpoint(cast(T, other))
        else:
            other = cast(Endpoint[T], other)
        if isinstance(other.value, Infinity):
            return other.value < self.value
        return self.value > other.value

    def __le__(self, other: object) -> bool:
        return not self > other

    def __ge__(self, other: object) -> bool:
        return not self < other
