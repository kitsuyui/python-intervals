from typing import cast, Generic, Iterable, List, TypeVar, Union

from abc import abstractmethod

from typing_extensions import Protocol

from intervals.endpoint import Endpoint
from intervals.comparable import Comparable


T = TypeVar('T', bound=Comparable, contravariant=True)


class IntervalProtocol(Protocol[T]):

    @abstractmethod
    def __contains__(self, object: T) -> bool:
        pass


class Interval(Generic[T]):
    intervals: List[IntervalProtocol[T]]

    def __init__(self, intervals: Iterable[IntervalProtocol[T]]) -> None:
        self.intervals = list(intervals)

    def __contains__(self, object: T) -> bool:
        return any(object in i for i in self.intervals)

    def __repr__(self) -> str:
        inner = ', '.join(repr(i) for i in self.intervals)
        return f'<Interval {inner}>'


class SingleInterval(Generic[T]):
    left: Endpoint[T]
    right: Endpoint[T]

    def __init__(self,
                 left: Union[T, Endpoint[T]],
                 right: Union[T, Endpoint[T]]) -> None:
        if not isinstance(left, Endpoint):
            left = Endpoint(cast(T, left))
        else:
            left = cast(Endpoint[T], left)
        if not isinstance(right, Endpoint):
            right = Endpoint(cast(T, right))
        else:
            right = cast(Endpoint[T], right)
        right = cast(Endpoint[T], right)
        assert left <= right
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        leftparen = '(' if self.left.open else '['
        rightparen = ')' if self.right.open else ']'
        return f'{leftparen}{self.left.value}, {self.right.value}{rightparen}'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented
        return all((
            self.left == other.left,
            self.right == other.right,
        ))

    def __lt__(self, other: object) -> bool:
        if self.right.open:
            return self.right <= other
        return self.right < other

    def __gt__(self, other: object) -> bool:
        if self.left.open:
            return self.left >= other
        return self.left > other

    def __le__(self, other: object) -> bool:
        if self == other:
            return True
        if self.right.open:
            return self.right < other
        return self.right <= other

    def __ge__(self, other: object) -> bool:
        if self == other:
            return True
        if self.left.open:
            return self.left > other
        return self.left >= other

    def __contains__(self, other: Union[T, Endpoint[T]]) -> bool:
        if not isinstance(other, Endpoint):
            other = Endpoint(cast(T, other))
        else:
            other = cast(Endpoint[T], other)
        return not(self > other or self < other)

    def __or__(self, other: 'SingleInterval[T]') -> 'IntervalProtocol[T]':
        if any((
            other.left in self or other.right in self,
            self.left in other or self.right in other,
        )):
            return SingleInterval(
                min(self.left, other.left),
                max(self.right, other.right),
            )
        return Interval([self, other])

    def __and__(self, other: 'SingleInterval[T]') -> 'IntervalProtocol[T]':
        if any((
            other.left in self or other.right in self,
            self.left in other or self.right in other,
        )):
            return SingleInterval(
                max(self.left, other.left),
                min(self.right, other.right),
            )
        return Interval([])
