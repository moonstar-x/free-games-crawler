import pkg.crawling.crawler as module
from typing import cast


class TestCrawler:
    class TestRun:
        def test_should_return_crawl(self):
            class ConcreteCrawler(module.Crawler):
                def _crawl(self):
                    return 'stuff'

            crawler = ConcreteCrawler()

            assert crawler.run() == 'stuff'


class TestHttpCrawler:
    class TestRun:
        def test_should_return_crawl(self):
            class ConcreteCrawler(module.HttpCrawler):
                def _crawl(self):
                    return 'stuff'

            crawler = ConcreteCrawler(cast(module.HttpClient, None))

            assert crawler.run() == 'stuff'
