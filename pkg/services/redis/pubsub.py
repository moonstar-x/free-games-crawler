from pkg.services.redis.client import create_client
from pkg.models.offer import Offer
from pkg.services.redis import PUBSUB_OFFER_CHANNEL


def publish_offer(offer: Offer) -> None:
    with create_client() as client:
        client.publish(PUBSUB_OFFER_CHANNEL, offer.to_json())
