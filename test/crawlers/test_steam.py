import pkg.crawlers.steam as module
import pytest
import pathlib
from pkg.models.offer import Offer


@pytest.fixture(scope='session')
def mocked_steam_listing():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/steam_listing.txt')

    with filepath.open('r') as file:
        return file.read()


@pytest.fixture(scope='session')
def mocked_steam_page_dlc():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/steam_page_dlc.txt')

    with filepath.open('r') as file:
        return file.read()


@pytest.fixture(scope='session')
def mocked_steam_page_game():
    cur_directory = pathlib.Path(__file__).parent.resolve()
    filepath = cur_directory.joinpath('__mocks__/steam_page_game.txt')

    with filepath.open('r') as file:
        return file.read()


@pytest.fixture
def crawler(mocked_steam_listing, mocked_steam_page_dlc, mocked_steam_page_game, mocker):
    mock_client = mocker.MagicMock()
    mock_client.get_html.side_effect = [
        module.HttpClient.parse_html(mocked_steam_listing),
        module.HttpClient.parse_html(mocked_steam_page_game),
        module.HttpClient.parse_html(mocked_steam_page_dlc)
    ]

    return module.SteamCrawler(mock_client)


class TestSteamCrawler:
    class TestRun:
        def test_should_return_offers(self, crawler):
            result = list(crawler.run())

            offer_1 = Offer(
                storefront='Steam',
                id='442070',
                url='https://store.steampowered.com/app/442070/Drawful_2/?snr=1_7_7_2300_150_1',
                title='Drawful 2',
                description='For 3-8 players and an audience of thousands! Your phones or tablets are your controllers! The game of terrible drawings and hilariously wrong answers.',
                type='game',
                publisher='Jackbox Games',
                original_price=5.79,
                original_price_fmt='$5.79 USD',
                thumbnail='https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/442070/header.jpg?t=1721927113'
            )

            offer_2 = Offer(
                storefront='Steam',
                id='3101570',
                url='https://store.steampowered.com/app/3101570/Minion_Masters__Power_UP/?snr=1_7_7_2300_150_1',
                title='Minion Masters - Power UP',
                description='The Power UP! DLC is a great +300% value bundle emphasising flexibility to let you adapt to the changing fates of battle! You also get a headstart in the Season Pass!',
                type='dlc',
                publisher='Betadwarf',
                original_price=7.99,
                original_price_fmt='$7.99 USD',
                thumbnail='https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3101570/header.jpg?t=1721923409'
            )

            assert result[0] == offer_1
            assert result[1] == offer_2


class TestBuilder:
    def test_should_have_correct_name(self):
        assert module.Builder.NAME == 'Steam'

    class TestMake:
        def test_should_return_valid_instance(self):
            assert isinstance(module.Builder.make(), module.SteamCrawler)
