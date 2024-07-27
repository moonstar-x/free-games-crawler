import pkg.config as module
import pytest
import importlib


def assert_config(config: module.Config) -> None:
    assert config.redis_uri == 'redis://localhost:6379'
    assert config.http_request_timeout == 0.5
    assert config.http_max_retries == 10
    assert config.http_retry_timeout == 3
    assert config.threading_enabled is True
    assert config.threading_max_workers == 5


@pytest.fixture
def set_env_vars(monkeypatch):
    monkeypatch.setenv('REDIS_URI', 'redis://localhost:6379')
    monkeypatch.setenv('CRAWLER_HTTP_REQUEST_TIMEOUT', '0.5')
    monkeypatch.setenv('CRAWLER_HTTP_MAX_RETRIES', '10')
    monkeypatch.setenv('CRAWLER_HTTP_RETRY_TIMEOUT', '3')
    monkeypatch.setenv('THREADING_ENABLED', 'true')
    monkeypatch.setenv('THREADING_MAX_WORKERS', '5')
    yield


class TestConfig:
    class TestFromEnv:
        def test_should_create_config_from_env(self, set_env_vars):
            config = module.Config.from_env()
            assert_config(config)

    class TestConfig:
        def test_should_return_config_from_env(self, set_env_vars):
            importlib.reload(module)
            assert_config(module.config)
