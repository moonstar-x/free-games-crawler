import pkg.crawlers.epicgames as module
import pytest
import pathlib
import json


@pytest.fixture
def mocked_data():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/epic_games_response.txt')

    with filepath.open('r') as file:
        return json.loads(file.read())


class TestEpicGamesCrawler:
    class TestRun:
        def test_should_return_offers(self, mocked_data):
            pass


class TestBuilder:
    def test_should_have_correct_name(self):
        assert module.Builder.NAME == 'EpicGames'

    class TestMake:
        def test_should_return_valid_instance(self):
            assert isinstance(module.Builder.make(), module.EpicGamesCrawler)
