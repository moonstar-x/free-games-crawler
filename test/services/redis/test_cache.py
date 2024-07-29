import pkg.services.redis.cache as module
import pytest
from typing import cast
from pkg.models.offer import Offer


class Mocks:
    class OfferMock:
        @staticmethod
        def get_cache_key():
            return 'key'

        @staticmethod
        def to_json():
            return 'json_data'


@pytest.fixture
def mock_config(mocker):
    mock_config = mocker.patch('pkg.services.redis.cache.config')
    mock_config.redis_ttl = 10

    return mock_config


@pytest.fixture
def mock_client(mocker, mock_config):
    mock_client = mocker.patch('pkg.services.redis.cache.create_client')
    return mock_client.return_value.__enter__.return_value


class TestCacheInsertOffer:
    def test_should_call_set_with_offer(self, mock_client):
        offer = cast(Offer, Mocks.OfferMock())
        module.cache_insert_offer(offer)

        mock_client.set.assert_called_with('key', 'json_data', ex=10)


class TestCacheOfferExists:
    def test_should_return_if_exists(self, mock_client):
        mock_client.exists.return_value = True
        result = module.cache_offer_exists('key')

        assert result is True
