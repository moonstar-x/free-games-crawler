import pkg.crawling.factory as module
from typing import cast


class TestCrawlerFactory:
    class TestGetAll:
        def test_should_return_list_of_crawlers(self, mocker):
            mocked_crawler_builders = [mocker.Mock(), mocker.Mock()]
            mocked_crawler_builders_dict = {
                '1': lambda **kwargs: mocked_crawler_builders[0],
                '2': lambda **kwargs: mocked_crawler_builders[1]
            }
            mocker.patch('pkg.crawling.factory.get_crawlers', return_value=mocked_crawler_builders_dict)

            factory = module.CrawlerFactory(cast(module.HttpClientOptions, None))
            result = factory.get_all()

            assert len(result) == 2
            assert result[0] == mocked_crawler_builders[0]
            assert result[1] == mocked_crawler_builders[1]
