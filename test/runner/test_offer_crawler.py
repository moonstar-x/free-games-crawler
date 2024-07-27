import pkg.runner.offer_crawler as module
import pytest


@pytest.fixture
def runner(mocker):
    crawler = mocker.MagicMock()
    return module.OfferCrawlerRunner(crawler)


class TestOfferCrawlerRunner:
    class TestRun:
        def test_should_log_start(self, runner):
            runner.run()
            runner._crawler.logger.log.assert_any_call('Crawling started...')

        def test_should_log_end(self, runner):
            runner.run()
            runner._crawler.logger.log.assert_any_call('Crawling ended.')

        def test_should_log_exception_if_occurs(self, runner, mocker):
            error = Exception('Oops')

            with mocker.patch.object(runner, '_execute', side_effect=error):
                runner.run()

                runner._crawler.logger.log.assert_any_call('An error occurred while crawling.')
                runner._crawler.logger.exception.assert_any_call(error)
