import pkg.services.redis.pubsub as module
import pytest
from typing import cast
from pkg.models.offer import Offer


class Mocks:
    class OfferMock:
        @staticmethod
        def to_json():
            return 'json_data'


@pytest.fixture
def mock_client(mocker):
    mock_client = mocker.patch('pkg.services.redis.pubsub.create_client')
    return mock_client.return_value.__enter__.return_value


class TestPublishOffer:
    def test_should_publish_offer(self, mock_client):
        offer = cast(Offer, Mocks.OfferMock())
        module.publish_offer(offer)

        mock_client.publish.assert_called_with('offers', 'json_data')
