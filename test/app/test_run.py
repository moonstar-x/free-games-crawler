import pkg.app.run as module
from unittest.mock import call


class TestRunCrawlers:
    def test_should_push_crawlers_and_start(self, mocker):
        mock_crawler_factory = mocker.patch('pkg.app.run.CrawlerFactory')
        mocked_crawlers = [mocker.Mock(), mocker.Mock()]
        mock_crawler_factory.return_value.get_all.return_value = mocked_crawlers

        mock_runner_executor = mocker.patch('pkg.app.run.RunnerExecutor')
        mock_offer_crawler_runner = mocker.patch('pkg.app.run.OfferCrawlerRunner')

        module.run_crawlers()

        mock_offer_crawler_runner.assert_has_calls([call(crawler) for crawler in mocked_crawlers])
        mock_runner_executor.return_value.push.assert_has_calls([call(mock_offer_crawler_runner.return_value) for _ in mocked_crawlers])
        mock_runner_executor.return_value.start.assert_called_once()
