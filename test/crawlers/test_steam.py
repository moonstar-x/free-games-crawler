import pkg.crawlers.steam as module
import pytest
import pathlib
from pkg.models.offer import Offer


@pytest.fixture(scope='session')
def mocked_steam_listing_dlc():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/steam_listing_dlc.txt')

    with filepath.open('r') as file:
        return file.read()


@pytest.fixture(scope='session')
def mocked_steam_page_dlc():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/steam_page_dlc.txt')

    with filepath.open('r') as file:
        return file.read()


@pytest.fixture
def crawler_dlc(mocked_steam_listing_dlc, mocked_steam_page_dlc, mocker):
    mock_client = mocker.MagicMock()
    mock_client.get_html.side_effect = [module.HttpClient.parse_html(mocked_steam_listing_dlc), module.HttpClient.parse_html(mocked_steam_page_dlc)]

    return module.SteamCrawler(mock_client)


# TODO: Add a test for a base game once I can get a mock page source to use.
class TestSteamCrawler:
    class TestWithDlc:
        class TestRun:
            def test_should_return_offers(self, crawler_dlc):
                result = list(crawler_dlc.run())

                offer = Offer(
                    storefront='Steam',
                    url='https://store.steampowered.com/app/3101570/Minion_Masters__Power_UP/?snr=1_7_7_2300_150_1',
                    title='Minion Masters - Power UP',
                    description='The Power UP! DLC is a great +300% value bundle emphasising flexibility to let you adapt to the changing fates of battle! You also get a headstart in the Season Pass!',
                    type='dlc',
                    publisher='Betadwarf',
                    original_price=7.99,
                    original_price_fmt='$7.99 USD',
                    thumbnail='https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3101570/header.jpg?t=1721923409'
                )

                assert result[0] == offer


class TestBuilder:
    def test_should_have_correct_name(self):
        assert module.Builder.NAME == 'Steam'

    class TestMake:
        def test_should_return_valid_instance(self):
            assert isinstance(module.Builder.make(), module.SteamCrawler)
