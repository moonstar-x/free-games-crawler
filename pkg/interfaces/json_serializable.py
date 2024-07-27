from typing import Protocol
from abc import abstractmethod


class JsonSerializable(Protocol):
    @abstractmethod
    def to_json(self) -> str:
        raise NotImplemented
