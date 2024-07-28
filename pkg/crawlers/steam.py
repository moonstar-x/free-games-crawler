import re
from typing import Iterator
from bs4 import BeautifulSoup
from pkg.crawling.crawler import HttpCrawler
from pkg.crawling.client.http import HttpClient
from pkg.models.offer import Offer, OfferType
from pkg.utils.lang import safe_attribute_chain


class SteamCrawler(HttpCrawler[Iterator[Offer]]):
    STOREFRONT_NAME = 'Steam'

    def __init__(self, client: HttpClient):
        super().__init__(client)

        self._listing_url = 'https://store.steampowered.com/search/?maxprice=free&specials=1'
        self._cookies = {
            'lastagecheckage': '1-January-1999',
            'birthtime': '915170401',
            'wants_mature_content': '1'
        }

    def _crawl(self):
        response = self._client.get_html(self._listing_url, cookies=self._cookies)
        return self._extract_offers(response)

    def _extract_offers(self, soup: BeautifulSoup) -> Iterator[Offer]:
        items = soup.find_all(attrs={'id': 'search_resultsRows'})

        for item in items:
            yield self._get_offer_for_item(item)

    def _get_offer_for_item(self, item: BeautifulSoup) -> Offer:
        url = item.find('a').attrs.get('href')
        soup = self._client.get_html(url, cookies=self._cookies)

        return self._map_offer(url, soup)

    def _map_offer(self, url: str, soup: BeautifulSoup) -> Offer:
        title = soup.find('div', attrs={'id': 'appHubAppName'}).get_text()
        description = soup.find('meta', attrs={'property': 'og:description'}).attrs.get('content')
        offer_type = self._resolve_offer_type(soup)

        publisher = safe_attribute_chain(lambda: soup.find_all('div', attrs={'class': 'dev_row'})[-1].find('a').get_text())
        original_price_fmt = safe_attribute_chain(lambda: soup.find('div', attrs={'class': 'discount_original_price'}).get_text())

        price_pattern = r'(\d+\.?\d*)'
        original_price_match = re.search(price_pattern, original_price_fmt) if original_price_fmt else None
        original_price_str = original_price_match.group(1) if original_price_match else None
        original_price = float(original_price_str) if original_price_str else None

        thumbnail = safe_attribute_chain(lambda: soup.find('img', attrs={'class': 'game_header_image_full'}).attrs.get('src'))

        return Offer(
            storefront=SteamCrawler.STOREFRONT_NAME,
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
    def _resolve_offer_type(soup: BeautifulSoup) -> OfferType:
        dlc_bubble = soup.find('div', attrs={'class': 'game_area_dlc_bubble'})
        if dlc_bubble:
            return 'dlc'

        soundtrack_bubble = soup.find('div', attrs={'class': 'game_area_soundtrack_bubble'})
        if soundtrack_bubble:
            return 'other'

        return 'game'


class Builder:
    NAME = SteamCrawler.STOREFRONT_NAME

    @staticmethod
    def make(**kwargs) -> SteamCrawler:
        return SteamCrawler(kwargs.get('http_client'))
