from __future__ import annotations
import os
from typing import Optional, Union, Literal
from dataclasses import dataclass
from pkg.utils.lang import safe_float, safe_int


@dataclass
class Config:
    redis_uri: str
    redis_ttl: int

    http_request_timeout: Optional[float]
    http_max_retries: Optional[int]
    http_retry_timeout: Optional[float]

    threading_enabled: Optional[bool]
    threading_max_workers: Optional[Union[int, Literal['auto']]]

    @staticmethod
    def from_env() -> Config:
        return Config(
            redis_uri=os.getenv('REDIS_URI'),
            redis_ttl=safe_int(os.getenv('REDIS_TTL')),
            http_request_timeout=safe_float(os.getenv('CRAWLER_HTTP_REQUEST_TIMEOUT')),
            http_max_retries=safe_int(os.getenv('CRAWLER_HTTP_MAX_RETRIES')),
            http_retry_timeout=safe_float(os.getenv('CRAWLER_HTTP_RETRY_TIMEOUT')),
            threading_enabled=os.getenv('THREADING_ENABLED') == 'true',
            threading_max_workers=safe_int(os.getenv('THREADING_MAX_WORKERS'))
        )


config = Config.from_env()
