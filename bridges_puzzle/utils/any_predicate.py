from typing import TypeVar, Callable, Iterable


T = TypeVar("T")


def any_predicate(lst: Iterable[T], predicate: Callable[[T], bool]) -> bool:
    for item in lst:
        if predicate(item):
            return True

    return False
