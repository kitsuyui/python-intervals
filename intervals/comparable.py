from abc import abstractmethod
from typing import Any, TypeVar

from typing_extensions import Protocol


C = TypeVar('C', bound='Comparable')


class Comparable(Protocol):

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    @abstractmethod
    def __gt__(self: C, other: C) -> bool:
        pass

    @abstractmethod
    def __le__(self: C, other: C) -> bool:
        pass

    @abstractmethod
    def __ge__(self: C, other: C) -> bool:
        pass
