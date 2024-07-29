import pkg.runner.offer_crawler as module
import pytest


class Mocks:
    class OfferMock:
        @staticmethod
        def get_cache_key():
            return 'key'

        @staticmethod
        def to_str():
            return 'offer_str'


@pytest.fixture
def offer():
    return Mocks.OfferMock()


@pytest.fixture
def runner(mocker, offer):
    crawler = mocker.MagicMock()
    crawler.run.return_value = [offer]
    return module.OfferCrawlerRunner(crawler)


@pytest.fixture
def mock_cache_insert_offer(mocker):
    return mocker.patch('pkg.runner.offer_crawler.cache_insert_offer')


@pytest.fixture
def mock_cache_offer_exists(mocker):
    return mocker.patch('pkg.runner.offer_crawler.cache_offer_exists')


@pytest.fixture
def mock_publish_offer(mocker):
    return mocker.patch('pkg.runner.offer_crawler.publish_offer')


class TestOfferCrawlerRunner:
    class TestRun:
        def test_should_log_start(self, runner, mock_cache_offer_exists, mock_cache_insert_offer, mock_publish_offer):
            runner.run()
            runner._crawler.logger.info.assert_any_call('Crawling started...')

        def test_should_log_end(self, runner, mock_cache_offer_exists, mock_cache_insert_offer, mock_publish_offer):
            runner.run()
            runner._crawler.logger.info.assert_any_call('Crawling ended.')

        def test_should_log_exception_if_occurs(self, runner, mocker, mock_cache_offer_exists, mock_cache_insert_offer, mock_publish_offer):
            error = Exception('Oops')

            with mocker.patch.object(runner, '_execute', side_effect=error):
                runner.run()

                runner._crawler.logger.info.assert_any_call('An error occurred while crawling.')
                runner._crawler.logger.exception.assert_any_call(error)

        def test_should_log_about_existing_offer(self, runner, mock_cache_offer_exists, mock_cache_insert_offer):
            mock_cache_offer_exists.return_value = True
            runner.run()
            runner._crawler.logger.info.assert_any_call('Found existing offer: offer_str - Will update cache and skip publish.')

        def test_should_insert_existing_offer(self, runner, offer, mock_cache_offer_exists, mock_cache_insert_offer):
            mock_cache_offer_exists.return_value = True
            runner.run()
            mock_cache_insert_offer.assert_called_with(offer)

        def test_should_log_about_new_offer(self, runner, mock_cache_offer_exists, mock_cache_insert_offer, mock_publish_offer):
            mock_cache_offer_exists.return_value = False
            runner.run()
            runner._crawler.logger.info.assert_any_call('Found new offer: offer_str - Will update cache and publish.')

        def test_should_insert_new_offer(self, runner, offer, mock_cache_offer_exists, mock_cache_insert_offer, mock_publish_offer):
            mock_cache_offer_exists.return_value = False
            runner.run()
            mock_cache_insert_offer.assert_called_with(offer)

        def test_should_publish_new_offer(self, runner, offer, mock_cache_offer_exists, mock_cache_insert_offer, mock_publish_offer):
            mock_cache_offer_exists.return_value = False
            runner.run()
            mock_publish_offer.assert_called_with(offer)
