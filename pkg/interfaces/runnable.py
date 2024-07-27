from typing import Protocol
from abc import abstractmethod


class Runnable(Protocol):
    @abstractmethod
    def run(self) -> None:
        raise NotImplemented
