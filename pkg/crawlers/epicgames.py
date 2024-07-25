from typing import Iterator
from pkg.crawling.crawler import HttpCrawler
from pkg.crawling.client.http import HttpClient
from pkg.models.offer import Offer


class EpicGamesCrawler(HttpCrawler[Iterator[Offer]]):
    STOREFRONT_NAME = 'EpicGames'

    def __init__(self, client: HttpClient):
        super().__init__(client)

        self._base_url = 'https://store-site-backend-static.ak.epicgames.com'

    def _crawl(self):
        yield self._client.get_json(f'{self._base_url}/freeGamesPromotions')


class Builder:
    NAME = EpicGamesCrawler.STOREFRONT_NAME

    @staticmethod
    def make(**kwargs) -> EpicGamesCrawler:
        return EpicGamesCrawler(kwargs.get('http_client'))
