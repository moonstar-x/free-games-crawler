from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from pkg.crawling.client.http import HttpClient
from pkg.utils.lang import get_class_name
from pkg.utils.log import Logger


_T = TypeVar('_T')


class Crawler(ABC, Generic[_T]):
    def __init__(self):
        self._logger = Logger(get_class_name(self))

    @property
    def logger(self) -> Logger:
        return self._logger

    @abstractmethod
    def _crawl(self) -> _T:
        raise NotImplemented

    def run(self) -> _T:
        return self._crawl()


class HttpCrawler(Crawler[_T], ABC):
    def __init__(self, client: HttpClient):
        super().__init__()
        self._client = client
