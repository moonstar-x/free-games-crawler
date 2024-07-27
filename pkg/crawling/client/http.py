from __future__ import annotations
import requests
import requests.utils
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from typing import Callable, TypeVar, Any, Dict, Union, Optional, overload
from dataclasses import dataclass
from time import sleep
from pkg.utils.lang import Json
from pkg.config import Config


_T = TypeVar('_T')


@dataclass
class HttpClientOptions:
    request_timeout: float
    max_retries: int
    retry_timeout: float

    @staticmethod
    def from_config(config: Config) -> HttpClientOptions:
        return HttpClientOptions(
            request_timeout=config.http_request_timeout if config.http_request_timeout is not None else 0,
            max_retries=config.http_max_retries if config.http_max_retries is not None else 10,
            retry_timeout=config.http_retry_timeout if config.http_retry_timeout is not None else 0.5,
        )


class HttpClient:
    def __init__(self, options: HttpClientOptions):
        self._options = options

        self._headers = HttpClient._prepare_headers({})

    def set_headers(self, headers: Dict[str, str]) -> None:
        self._headers = HttpClient._prepare_headers(headers)

    def get_html(self, url: str, **kwargs) -> BeautifulSoup:
        response = self._with_retry(self._get, url, **kwargs)
        return HttpClient.parse_html(response.content)

    def post_html(self, url: str, **kwargs) -> BeautifulSoup:
        response = self._with_retry(self._post, url, **kwargs)
        return HttpClient.parse_html(response.content)

    def get_json(self, url: str, **kwargs) -> Json:
        response = self._with_retry(self._get, url, **kwargs)
        return response.json()

    def post_json(self, url: str, **kwargs) -> Json:
        response = self._with_retry(self._post, url, **kwargs)
        return response.json()

    @overload
    def get_raw(self, url: str, encoding: None, **kwargs) -> bytes:
        ...

    @overload
    def get_raw(self, url: str, encoding: str, **kwargs) -> str:
        ...

    @overload
    def get_raw(self, url: str, **kwargs) -> str:
        ...

    def get_raw(self, url: str, encoding: Optional[str] = 'utf-8', **kwargs) -> Union[str, bytes]:
        response = self._with_retry(self._get, url, **kwargs)

        if encoding is not None:
            return response.content.decode(encoding)

        return response.content

    @overload
    def post_raw(self, url: str, encoding: None, **kwargs) -> bytes:
        ...

    @overload
    def post_raw(self, url: str, encoding: str, **kwargs) -> str:
        ...

    @overload
    def post_raw(self, url: str, **kwargs) -> str:
        ...

    def post_raw(self, url: str, encoding: Optional[str] = 'utf-8', **kwargs) -> Union[str, bytes]:
        response = self._with_retry(self._post, url, **kwargs)

        if encoding is not None:
            return response.content.decode(encoding)

        return response.content

    # TODO: Sleep should be random?
    def _request_sleep(self) -> None:
        if self._options.request_timeout > 0:
            sleep(self._options.request_timeout)

    def _get(self, url: str, **kwargs) -> requests.Response:
        self._request_sleep()

        response = requests.get(url, headers=self._headers, **kwargs)
        response.raise_for_status()

        return response

    def _post(self, url: str, **kwargs) -> requests.Response:
        self._request_sleep()

        response = requests.post(url, headers=self._headers, **kwargs)
        response.raise_for_status()

        return response

    def _with_retry(self, fn: Callable[[Any], _T], *args, **kwargs) -> _T:
        handled_exception = None

        for _ in range(self._options.max_retries):
            try:
                return fn(*args, **kwargs)
            except Exception as error:
                handled_exception = error

                if self._options.retry_timeout > 0:
                    sleep(self._options.retry_timeout)

        raise handled_exception

    @staticmethod
    def parse_html(html: Union[str, bytes]) -> BeautifulSoup:
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def _prepare_headers(headers: Dict[str, str]) -> CaseInsensitiveDict[str]:
        complete_headers = requests.utils.default_headers()
        complete_headers.update(headers)

        return complete_headers
