from typing import Iterator
from pkg.crawling.crawler import Crawler
from pkg.models.offer import Offer
from pkg.runner.runnable import Runnable


class OfferCrawlerRunner(Runnable):
    def __init__(self, crawler: Crawler[Iterator[Offer]]):
        self._crawler = crawler

    def _execute(self) -> None:
        self._crawler.logger.log('Crawling started...')

        result = self._crawler.run()
        for offer in result:
            self._crawler.logger.log('Found offer', offer)

        self._crawler.logger.log('Crawling ended.')

    def run(self) -> None:
        try:
            self._execute()
        except Exception as error:
            self._crawler.logger.log('An error occurred while crawling.')
            self._crawler.logger.exception(error)
