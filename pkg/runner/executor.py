from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Union, Literal
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from pkg.interfaces.runnable import Runnable
from pkg.utils.log import Logger
from pkg.utils.lang import get_class_name
from pkg.config import Config


@dataclass
class RunnerExecutorOptions:
    enabled: bool
    max_workers: Union[int, Literal['auto']]

    @staticmethod
    def from_config(config: Config) -> RunnerExecutorOptions:
        return RunnerExecutorOptions(
            enabled=config.threading_enabled if config.threading_enabled is not None else True,
            max_workers=config.threading_max_workers if config.threading_max_workers is not None else 'auto'
        )


class RunnerExecutor:
    def __init__(self, options: RunnerExecutorOptions):
        self._runners = Queue()
        self._logger = Logger(get_class_name(self))

        self._options = options
        self._max_workers = RunnerExecutor._resolve_max_workers(options.max_workers)

    def push(self, runner: Runnable) -> None:
        self._runners.put(runner)

    def start(self) -> None:
        if self._options.enabled:
            return self._start_multi_thread()

        return self._start_single_thread()

    def _start_multi_thread(self) -> None:
        self._logger.info(f'Begin multi thread execution with {self._max_workers} workers.')

        with ThreadPoolExecutor(self._max_workers) as pool:
            while not self._runners.empty():
                runner = self._runners.get()
                pool.submit(runner.run)

    def _start_single_thread(self) -> None:
        self._logger.info(f'Begin single thread execution.')

        while not self._runners.empty():
            runner = self._runners.get()
            runner.run()

    @staticmethod
    def _resolve_max_workers(max_workers: Union[int, Literal['auto']]) -> int:
        if isinstance(max_workers, int):
            if max_workers < 1:
                raise ValueError('max_workers must be greater than or equal to 1.')

            return max_workers

        if isinstance(max_workers, str):
            if max_workers != 'auto':
                raise ValueError('max_workers must be an integer or "auto".')

            return os.cpu_count() or 1

        raise ValueError('max_workers must be an integer or "auto".')
