from pkg.services.redis.client import create_client
from pkg.models.offer import Offer
from pkg.config import config


def cache_insert_offer(offer: Offer) -> None:
    with create_client() as client:
        key = offer.get_cache_key()
        client.set(key, offer.to_json(), ex=config.redis_ttl)


def cache_offer_exists(key: str) -> bool:
    with create_client() as client:
        return client.exists(key)
