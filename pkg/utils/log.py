import traceback
from typing import Sequence, Any


# TODO: Add log levels?
# TODO: Add timestamp?
class Logger:
    def __init__(self, tag: str):
        self._tag = tag

    def log(self, *args) -> None:
        return self._print(Logger._prepare_message(args))

    def exception(self, error: Exception) -> None:
        self._print(Logger._prepare_message([error, '\n', *traceback.format_exception(error)]))

    def _print(self, message: str) -> None:
        to_print = f'({self._tag}): {message}'
        print(to_print)

    @staticmethod
    def _prepare_message(args: Sequence[Any]) -> str:
        return ' '.join([str(arg) for arg in args])
