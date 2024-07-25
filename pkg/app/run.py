from pkg.config import config
from pkg.crawling.factory import CrawlerFactory
from pkg.crawling.client.http import HttpClientOptions
from pkg.runner.offer_crawler import OfferCrawlerRunner
from pkg.runner.executor import RunnerExecutor, RunnerExecutorOptions


def run_crawlers() -> None:
    http_client_options = HttpClientOptions.from_config(config)
    executor_options = RunnerExecutorOptions.from_config(config)

    crawler_factory = CrawlerFactory(http_client_options)
    crawlers = crawler_factory.get_all()

    executor = RunnerExecutor(executor_options)
    for crawler in crawlers:
        runner = OfferCrawlerRunner(crawler)

        executor.push(runner)

    executor.start()
