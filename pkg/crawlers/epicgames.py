from typing import Iterator
from pkg.crawling.crawler import HttpCrawler
from pkg.crawling.client.http import HttpClient
from pkg.models.offer import Offer, OfferType
from pkg.utils.lang import Json, safe_attribute_chain
from pkg.utils.list import list_find


class EpicGamesCrawler(HttpCrawler[Iterator[Offer]]):
    STOREFRONT_NAME = 'EpicGames'

    def __init__(self, client: HttpClient):
        super().__init__(client)

        self._base_url = 'https://store-site-backend-static.ak.epicgames.com'
        self._store_base_url = 'https://store.epicgames.com/p'

    def _crawl(self):
        response = self._client.get_json(f'{self._base_url}/freeGamesPromotions')
        return self._extract_offers(response.get('data', {}))

    def _extract_offers(self, data: Json) -> Iterator[Offer]:
        elements = safe_attribute_chain(lambda: data.get('Catalog').get('searchStore').get('elements'))
        free_elements = [element for element in elements if self._filter_free_element(element)]

        for element in free_elements:
            yield self._map_element_to_offer(element)

    @staticmethod
    def _filter_free_element(element: Json) -> bool:
        promotional_offers = safe_attribute_chain(lambda: element.get('promotions').get('promotionalOffers'), [])
        discount_price = safe_attribute_chain(lambda: element.get('price').get('totalPrice').get('discountPrice'))

        return len(promotional_offers) > 0 and discount_price == 0

    def _map_element_to_offer(self, element: Json) -> Offer:
        offer_mappings = element.get('offerMappings')
        slug = safe_attribute_chain(lambda: list_find(offer_mappings, lambda m: m.get('pageSlug') is not None).get('pageSlug')) or element.get('productSlug')
        url = f'{self._store_base_url}/{slug}'

        title = element.get('title')
        description = element.get('description')
        offer_type = self._resolve_offer_type(element)

        publisher = safe_attribute_chain(lambda: element.get('seller').get('name'))
        original_price = safe_attribute_chain(lambda: element.get('price').get('totalPrice').get('originalPrice') / 100)
        original_price_fmt = safe_attribute_chain(lambda: element.get('price').get('totalPrice').get('fmtPrice').get('originalPrice'))

        images = element.get('keyImages', [])
        thumbnail = safe_attribute_chain(lambda: list_find(images, lambda d: d.get('type') in ['Thumbnail', 'DieselStoreFrontWide']).get('url'))

        return Offer(
            storefront=EpicGamesCrawler.STOREFRONT_NAME,
            id=slug,
            url=url,
            title=title,
            description=description,
            type=offer_type,
            publisher=publisher,
            original_price=original_price,
            original_price_fmt=original_price_fmt,
            thumbnail=thumbnail
        )

    @staticmethod
    def _resolve_offer_type(element: Json) -> OfferType:
        offer_type = element.get('offerType')

        if offer_type == 'BASE_GAME':
            return 'game'

        if offer_type == 'ADD_ON' or offer_type == 'VIRTUAL_CURRENCY':
            return 'dlc'

        if offer_type == 'BUNDLE':
            return 'bundle'

        return 'other'


class Builder:
    NAME = EpicGamesCrawler.STOREFRONT_NAME

    @staticmethod
    def make(**kwargs) -> EpicGamesCrawler:
        return EpicGamesCrawler(kwargs.get('http_client'))
