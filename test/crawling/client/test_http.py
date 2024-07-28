import pkg.crawling.client.http as module
import pytest
from unittest.mock import call
import requests.models
import requests.exceptions
from collections import namedtuple
from typing import cast
from bs4 import BeautifulSoup
from pkg.config import Config


class Mocks:
    ConfigMock = namedtuple('ConfigMock', ['http_request_timeout', 'http_max_retries', 'http_retry_timeout'])


@pytest.fixture
def client():
    config = cast(Config, Mocks.ConfigMock(
        http_request_timeout=0,
        http_max_retries=1,
        http_retry_timeout=0
    ))
    options = module.HttpClientOptions.from_config(config)

    return module.HttpClient(options)


@pytest.fixture
def client_with_options():
    config = cast(Config, Mocks.ConfigMock(
        http_request_timeout=1,
        http_max_retries=5,
        http_retry_timeout=2
    ))
    options = module.HttpClientOptions.from_config(config)

    return module.HttpClient(options)


class TestHttpClientOptions:
    class TestFromConfig:
        def test_should_create_options_with_provided_values(self):
            config = cast(Config, Mocks.ConfigMock(
                http_request_timeout=1,
                http_max_retries=2,
                http_retry_timeout=3
            ))
            result = module.HttpClientOptions.from_config(config)

            assert result.request_timeout == 1
            assert result.max_retries == 2
            assert result.retry_timeout == 3

        def test_should_create_options_with_default_values(self):
            config = cast(Config, Mocks.ConfigMock(
                http_request_timeout=None,
                http_max_retries=None,
                http_retry_timeout=None
            ))
            result = module.HttpClientOptions.from_config(config)

            assert result.request_timeout == 0
            assert result.max_retries == 10
            assert result.retry_timeout == 0.5


@pytest.fixture
def mock_sleep(mocker):
    return mocker.patch('pkg.crawling.client.http.sleep')


@pytest.fixture
def mock_html(mocker):
    mock_response = mocker.MagicMock()
    mock_response.content = b'<html><head></head><body></body></html>'

    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('requests.post', return_value=mock_response)

    yield


@pytest.fixture
def mock_json(mocker):
    mock_response = mocker.MagicMock()
    mock_response.json.return_value = {'result': 'valid'}

    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('requests.post', return_value=mock_response)

    yield


@pytest.fixture
def mock_raw(mocker):
    mock_response = mocker.MagicMock()
    mock_response.content = b'response'

    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('requests.post', return_value=mock_response)

    yield


@pytest.fixture
def mock_status_error(mocker):
    mock_response = requests.models.Response()
    mock_response.status_code = 500

    mocker.patch('requests.get', return_value=mock_response)
    mocker.patch('requests.post', return_value=mock_response)

    yield


class TestHttpClient:
    class TestSetHeaders:
        def test_should_set_headers(self, client):
            client.set_headers({'Custom': 'Value'})
            assert client._headers.get('custom') == 'Value'

        def test_should_have_user_agent_regardless(self, client):
            client.set_headers({})
            assert client._headers.get('user-agent') == 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15'

    class TestGetHtml:
        def test_should_return_a_valid_beautiful_soup(self, client, mock_html):
            assert isinstance(client.get_html(''), BeautifulSoup)

        def test_should_raise_if_no_success_code(self, client, mock_status_error):
            with pytest.raises(requests.exceptions.HTTPError):
                client.get_html('')

        def test_should_not_sleep_when_requesting_if_no_timeout(self, client, mock_html, mock_sleep):
            client.get_html('')
            mock_sleep.assert_not_called()

        def test_should_sleep_when_requesting_if_timeout(self, client_with_options, mock_html, mock_sleep):
            client_with_options.get_html('')
            mock_sleep.assert_called_with(1)

        def test_should_retry_until_max_attempts_if_error(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.get', side_effect=Exception('Oops')) as spy_get:
                    client_with_options.get_html('')

                    spy_get.assert_has_calls([call('')] * 5)

        def test_should_wait_between_retries(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.get', side_effect=Exception('Oops')):
                    client_with_options.get_html('')

                    mock_sleep.assert_has_calls([call(2)] * 5)

    class TestPostHtml:
        def test_should_return_a_valid_beautiful_soup(self, client, mock_html):
            assert isinstance(client.post_html(''), BeautifulSoup)

        def test_should_raise_if_no_success_code(self, client, mock_status_error):
            with pytest.raises(requests.exceptions.HTTPError):
                client.post_html('')

        def test_should_not_sleep_when_requesting_if_no_timeout(self, client, mock_html, mock_sleep):
            client.post_html('')
            mock_sleep.assert_not_called()

        def test_should_sleep_when_requesting_if_timeout(self, client_with_options, mock_html, mock_sleep):
            client_with_options.post_html('')
            mock_sleep.assert_called_with(1)

        def test_should_retry_until_max_attempts_if_error(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.post', side_effect=Exception('Oops')) as spy_post:
                    client_with_options.post_html('')

                    spy_post.assert_has_calls([call('')] * 5)

        def test_should_wait_between_retries(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.post', side_effect=Exception('Oops')):
                    client_with_options.post_html('')

                    mock_sleep.assert_has_calls([call(2)] * 5)

    class TestGetJson:
        def test_should_return_a_valid_beautiful_soup(self, client, mock_json):
            result = client.get_json('')

            assert isinstance(result, dict)
            assert result.get('result') == 'valid'

        def test_should_raise_if_no_success_code(self, client, mock_status_error):
            with pytest.raises(requests.exceptions.HTTPError):
                client.get_json('')

        def test_should_not_sleep_when_requesting_if_no_timeout(self, client, mock_json, mock_sleep):
            client.get_json('')
            mock_sleep.assert_not_called()

        def test_should_sleep_when_requesting_if_timeout(self, client_with_options, mock_json, mock_sleep):
            client_with_options.get_json('')
            mock_sleep.assert_called_with(1)

        def test_should_retry_until_max_attempts_if_error(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.get', side_effect=Exception('Oops')) as spy_get:
                    client_with_options.get_json('')

                    spy_get.assert_has_calls([call('')] * 5)

        def test_should_wait_between_retries(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.get', side_effect=Exception('Oops')):
                    client_with_options.get_json('')

                    mock_sleep.assert_has_calls([call(2)] * 5)

    class TestPostJson:
        def test_should_return_a_valid_beautiful_soup(self, client, mock_json):
            result = client.post_json('')

            assert isinstance(result, dict)
            assert result.get('result') == 'valid'

        def test_should_raise_if_no_success_code(self, client, mock_status_error):
            with pytest.raises(requests.exceptions.HTTPError):
                client.post_json('')

        def test_should_not_sleep_when_requesting_if_no_timeout(self, client, mock_json, mock_sleep):
            client.post_json('')
            mock_sleep.assert_not_called()

        def test_should_sleep_when_requesting_if_timeout(self, client_with_options, mock_json, mock_sleep):
            client_with_options.post_json('')
            mock_sleep.assert_called_with(1)

        def test_should_retry_until_max_attempts_if_error(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.post', side_effect=Exception('Oops')) as spy_post:
                    client_with_options.post_json('')

                    spy_post.assert_has_calls([call('')] * 5)

        def test_should_wait_between_retries(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.post', side_effect=Exception('Oops')):
                    client_with_options.post_json('')

                    mock_sleep.assert_has_calls([call(2)] * 5)

    class TestGetRaw:
        def test_should_return_string_if_encoding_provided(self, client, mock_raw):
            result = client.get_raw('', encoding='utf-8')

            assert isinstance(result, str)
            assert result == 'response'

        def test_should_return_string_if_no_encoding_provided(self, client, mock_raw):
            result = client.get_raw('')

            assert isinstance(result, str)
            assert result == 'response'

        def test_should_return_bytes_if_encoding_provided_is_none(self, client, mock_raw):
            result = client.get_raw('', encoding=None)

            assert isinstance(result, bytes)
            assert result == b'response'

        def test_should_raise_if_no_success_code(self, client, mock_status_error):
            with pytest.raises(requests.exceptions.HTTPError):
                client.get_raw('')

        def test_should_not_sleep_when_requesting_if_no_timeout(self, client, mock_raw, mock_sleep):
            client.get_raw('')
            mock_sleep.assert_not_called()

        def test_should_sleep_when_requesting_if_timeout(self, client_with_options, mock_raw, mock_sleep):
            client_with_options.get_raw('')
            mock_sleep.assert_called_with(1)

        def test_should_retry_until_max_attempts_if_error(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.get', side_effect=Exception('Oops')) as spy_get:
                    client_with_options.get_raw('')

                    spy_get.assert_has_calls([call('')] * 5)

        def test_should_wait_between_retries(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.get', side_effect=Exception('Oops')):
                    client_with_options.get_raw('')

                    mock_sleep.assert_has_calls([call(2)] * 5)

    class TestPostRaw:
        def test_should_return_string_if_encoding_provided(self, client, mock_raw):
            result = client.post_raw('', encoding='utf-8')

            assert isinstance(result, str)
            assert result == 'response'

        def test_should_return_string_if_no_encoding_provided(self, client, mock_raw):
            result = client.post_raw('')

            assert isinstance(result, str)
            assert result == 'response'

        def test_should_return_bytes_if_encoding_provided_is_none(self, client, mock_raw):
            result = client.post_raw('', encoding=None)

            assert isinstance(result, bytes)
            assert result == b'response'

        def test_should_raise_if_no_success_code(self, client, mock_status_error):
            with pytest.raises(requests.exceptions.HTTPError):
                client.post_raw('')

        def test_should_not_sleep_when_requesting_if_no_timeout(self, client, mock_raw, mock_sleep):
            client.post_raw('')
            mock_sleep.assert_not_called()

        def test_should_sleep_when_requesting_if_timeout(self, client_with_options, mock_raw, mock_sleep):
            client_with_options.post_raw('')
            mock_sleep.assert_called_with(1)

        def test_should_retry_until_max_attempts_if_error(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.post', side_effect=Exception('Oops')) as spy_post:
                    client_with_options.post_raw('')

                    spy_post.assert_has_calls([call('')] * 5)

        def test_should_wait_between_retries(self, client_with_options, mock_sleep, mocker):
            with pytest.raises(Exception):
                with mocker.patch('requests.post', side_effect=Exception('Oops')):
                    client_with_options.post_raw('')

                    mock_sleep.assert_has_calls([call(2)] * 5)

    class TestParseHtml:
        def test_should_return_beautiful_soup(self, client):
            result = client.parse_html('<html><head></head><body></body></html>')

            assert isinstance(result, BeautifulSoup)
