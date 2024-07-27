import pkg.crawlers as module
import inspect


class Mocks:
    class Builder:
        NAME = 'Builder'

        def make(self):
            pass


class TestCrawlers:
    class TestGetCrawlers:
        def test_should_return_dict_with_crawlers(self, mocker):
            mocker.patch('os.listdir', return_value=['module.py'])
            mocker.patch('pkg.crawlers.importlib.import_module', return_value=Mocks)

            assert inspect.isfunction(module.get_crawlers().get('Builder'))
            assert not inspect.isfunction(module.get_crawlers().get('Unknown'))
