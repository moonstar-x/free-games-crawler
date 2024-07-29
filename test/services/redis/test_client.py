import pkg.services.redis.client as module
import pytest
import redis


@pytest.fixture
def mock_config(mocker):
    mock_config = mocker.patch('pkg.services.redis.client.config')
    mock_config.redis_uri = 'redis://localhost:6379'

    return mock_config


class TestCreateClient:
    def test_should_return_redis_client(self, mock_config):
        client = module.create_client()
        assert isinstance(client, redis.Redis)
