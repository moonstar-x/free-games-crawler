import pkg.crawling.exception as module


class TestCrawlerException:
    def test_should_be_instance_of_exception(self):
        assert isinstance(module.CrawlerException(), Exception)


class TestHttpClientException:
    def test_should_be_instance_of_exception(self):
        assert isinstance(module.HttpClientException(), Exception)
