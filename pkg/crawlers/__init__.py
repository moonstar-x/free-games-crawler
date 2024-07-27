import os
import importlib
from typing import Dict, Protocol
from pkg.crawling.crawler import Crawler
from pkg.crawling.client.http import HttpClient
from pkg.utils.lang import safe_attribute_chain


class MakeCallable(Protocol):
    def __call__(self, http_client: HttpClient) -> Crawler: ...


def get_crawlers() -> Dict[str, MakeCallable]:
    modules = [file for file in os.listdir(os.path.dirname(__file__)) if not file.startswith('__') and file.endswith('py')]

    imported_modules = [importlib.import_module(f'.{file.replace('.py', '')}', package=__name__) for file in modules]
    imported_builders = [safe_attribute_chain(lambda: module.Builder) for module in imported_modules]

    return dict([(Builder.NAME, Builder.make) for Builder in imported_builders])
