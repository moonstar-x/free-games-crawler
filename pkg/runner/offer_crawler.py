from typing import Iterator
from pkg.crawling.crawler import Crawler
from pkg.models.offer import Offer
from pkg.interfaces.runnable import Runnable
from pkg.services.redis.cache import cache_insert_offer, cache_offer_exists
from pkg.services.redis.pubsub import publish_offer


class OfferCrawlerRunner(Runnable):
    def __init__(self, crawler: Crawler[Iterator[Offer]]):
        self._crawler = crawler

    def _execute(self) -> None:
        self._crawler.logger.log('Crawling started...')

        result = self._crawler.run()
        for offer in result:
            offer_exists = cache_offer_exists(offer.get_cache_key())

            if offer_exists:
                self._handle_existing_offer(offer)
            else:
                self._handle_new_offer(offer)

        self._crawler.logger.log('Crawling ended.')

    def _handle_existing_offer(self, offer: Offer) -> None:
        self._crawler.logger.log(f'Found existing offer: {offer.to_str()} - Will update cache and skip publish.')
        cache_insert_offer(offer)

    def _handle_new_offer(self, offer: Offer) -> None:
        self._crawler.logger.log(f'Found new offer: {offer.to_str()} - Will update cache and publish.')
        cache_insert_offer(offer)
        publish_offer(offer)

    def run(self) -> None:
        try:
            self._execute()
        except Exception as error:
            self._crawler.logger.log('An error occurred while crawling.')
            self._crawler.logger.exception(error)
