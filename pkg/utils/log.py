import traceback
from typing import Sequence, Any
from datetime import datetime


class Logger:
    def __init__(self, tag: str):
        self._tag = tag

    def info(self, *args) -> None:
        return self._print('INFO', Logger._prepare_message(args))

    def exception(self, error: Exception) -> None:
        self._print('ERROR', Logger._prepare_message([error, '\n', *traceback.format_exception(error)]))

    def _print(self, level: str, message: str) -> None:
        now = self._now_formatted()
        to_print = f'({self._tag} @ {now}): [{level}] - {message}'
        print(to_print)

    @staticmethod
    def _now_formatted() -> str:
        return datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')

    @staticmethod
    def _prepare_message(args: Sequence[Any]) -> str:
        return ' '.join([str(arg) for arg in args])
