from typing import NamedTuple, Generator, TypeVar, Callable, Iterable


T = TypeVar("T")


def has(lst: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    for item in lst:
        if predicate(item):
            return True

    return False
