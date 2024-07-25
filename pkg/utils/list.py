from typing import Callable, TypeVar, Any, List, Optional
from operator import indexOf


_T = TypeVar('_T')


def list_find(arr: List[_T], predicate: Callable[[_T], Any]) -> Optional[_T]:
    try:
        idx = indexOf(map(lambda e: bool(predicate(e)), arr), True)
        return arr[idx] if idx >= 0 else None
    except ValueError:
        return None
