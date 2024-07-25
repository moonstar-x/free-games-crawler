from typing import List
from pkg.crawling.client.http import HttpClient, HttpClientOptions
from pkg.crawling.crawler import Crawler
from pkg.crawlers import crawler_builders


class CrawlerFactory:
    def __init__(self, http_client_options: HttpClientOptions):
        self._http_client_options = http_client_options

    def get_all(self) -> List[Crawler]:
        http_client = HttpClient(self._http_client_options)

        return [make(http_client=http_client) for make in crawler_builders.values()]
